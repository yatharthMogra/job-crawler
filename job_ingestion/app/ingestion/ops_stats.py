from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.ingestion.fetch_backpressure import evaluate_backpressure, get_pending_queue_depth


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def collect_ops_stats(
    db: AsyncSession,
    *,
    settings: Settings,
    trigger: str = "manual",
) -> dict[str, Any]:
    now = _utcnow()
    since_24h = now - timedelta(hours=24)
    since_1h = now - timedelta(hours=1)
    since_5m = now - timedelta(minutes=5)

    jobs = (
        await db.execute(
            text(
                """
                SELECT
                  COUNT(*) FILTER (WHERE is_active) AS active,
                  COUNT(*) FILTER (WHERE is_active AND processing_state = 'success') AS enriched,
                  COUNT(*) FILTER (WHERE is_active AND processing_state = 'pending') AS pending,
                  COUNT(*) FILTER (WHERE is_active AND processing_state = 'partial_success') AS partial,
                  COUNT(*) FILTER (WHERE is_active AND processing_state = 'failed') AS failed
                FROM normalized_jobs
                """
            )
        )
    ).one()

    fetch_24h = (
        await db.execute(
            text(
                """
                SELECT
                  COUNT(*) AS pipeline_runs,
                  COALESCE(SUM(jobs_new), 0) AS jobs_new,
                  COALESCE(SUM(jobs_updated), 0) AS jobs_updated,
                  COALESCE(SUM(jobs_fetched), 0) AS jobs_fetched,
                  COALESCE(SUM(successful_companies), 0) AS companies_succeeded,
                  COALESCE(SUM(failed_companies), 0) AS companies_failed
                FROM pipeline_runs
                WHERE started_at >= :since
                """
            ),
            {"since": since_24h},
        )
    ).one()

    latest_run = (
        await db.execute(
            text(
                """
                SELECT
                  id,
                  run_type,
                  status,
                  started_at,
                  completed_at,
                  total_companies,
                  successful_companies,
                  failed_companies,
                  jobs_new,
                  jobs_updated,
                  jobs_fetched,
                  schedule_metadata
                FROM pipeline_runs
                ORDER BY started_at DESC
                LIMIT 1
                """
            )
        )
    ).first()

    queue_rows = (
        await db.execute(
            text(
                """
                SELECT status, COUNT(*)::int AS count
                FROM enrichment_queue
                GROUP BY status
                ORDER BY count DESC
                """
            )
        )
    ).all()
    queue = {str(status): int(count) for status, count in queue_rows}

    enrichment_windows = (
        await db.execute(
            text(
                """
                SELECT
                  COUNT(*) FILTER (
                    WHERE status = 'completed' AND updated_at >= :since_5m
                  ) AS completed_5m,
                  COUNT(*) FILTER (
                    WHERE status = 'completed' AND updated_at >= :since_1h
                  ) AS completed_1h,
                  COUNT(*) FILTER (
                    WHERE status IN ('failed', 'quota_blocked') AND updated_at >= :since_1h
                  ) AS failed_1h,
                  MAX(updated_at) FILTER (WHERE status = 'completed') AS last_completion
                FROM enrichment_queue
                """
            ),
            {"since_5m": since_5m, "since_1h": since_1h},
        )
    ).one()

    recent_polls = (
        await db.execute(
            text(
                """
                SELECT
                  c.name AS company,
                  c.board_token,
                  c.platform,
                  c.fetch_tier,
                  crr.status,
                  crr.jobs_new,
                  crr.jobs_updated,
                  crr.jobs_fetched,
                  crr.started_at,
                  crr.completed_at,
                  c.last_successful_fetch_at
                FROM company_run_results crr
                JOIN companies c ON c.id = crr.company_id
                ORDER BY crr.completed_at DESC
                LIMIT 40
                """
            )
        )
    ).all()

    keys = settings.gemini_api_keys_list()
    worker_count = settings.resolved_enrichment_worker_count() if keys else 0

    pending_depth = await get_pending_queue_depth(db)
    backpressure_decision = evaluate_backpressure(pending_depth, settings=settings)

    return {
        "generated_at": now.isoformat(),
        "trigger": trigger,
        "enrichment_workers": worker_count,
        "fetch_backpressure": {
            "enabled": backpressure_decision.enabled,
            "active": backpressure_decision.active,
            "depth": backpressure_decision.depth,
            "threshold": backpressure_decision.threshold,
            "mode": backpressure_decision.mode,
            "skip_tiers": sorted(backpressure_decision.skip_tiers),
            "allow_waas": backpressure_decision.allow_waas,
        },
        "jobs": {
            "active": int(jobs.active or 0),
            "enriched": int(jobs.enriched or 0),
            "pending_enrichment": int(jobs.pending or 0),
            "partial_success": int(jobs.partial or 0),
            "failed": int(jobs.failed or 0),
        },
        "fetch": {
            "last_24h": {
                "pipeline_runs": int(fetch_24h.pipeline_runs or 0),
                "jobs_new": int(fetch_24h.jobs_new or 0),
                "jobs_updated": int(fetch_24h.jobs_updated or 0),
                "jobs_fetched": int(fetch_24h.jobs_fetched or 0),
                "companies_succeeded": int(fetch_24h.companies_succeeded or 0),
                "companies_failed": int(fetch_24h.companies_failed or 0),
            },
            "latest_run": _serialize_latest_run(latest_run),
        },
        "enrichment": {
            "queue": queue,
            "completed_last_5m": int(enrichment_windows.completed_5m or 0),
            "completed_last_1h": int(enrichment_windows.completed_1h or 0),
            "failed_last_1h": int(enrichment_windows.failed_1h or 0),
            "last_completion": (
                enrichment_windows.last_completion.isoformat()
                if enrichment_windows.last_completion
                else None
            ),
        },
        "recent_company_polls": [
            {
                "company": row.company,
                "board_token": row.board_token,
                "platform": row.platform,
                "fetch_tier": row.fetch_tier,
                "status": row.status,
                "jobs_new": int(row.jobs_new or 0),
                "jobs_updated": int(row.jobs_updated or 0),
                "jobs_fetched": int(row.jobs_fetched or 0),
                "polled_at": row.completed_at.isoformat() if row.completed_at else None,
                "last_successful_fetch_at": (
                    row.last_successful_fetch_at.isoformat()
                    if row.last_successful_fetch_at
                    else None
                ),
            }
            for row in recent_polls
        ],
    }


def _serialize_latest_run(row: Optional[Any]) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    return {
        "id": str(row.id),
        "run_type": row.run_type,
        "status": row.status,
        "started_at": row.started_at.isoformat() if row.started_at else None,
        "completed_at": row.completed_at.isoformat() if row.completed_at else None,
        "total_companies": int(row.total_companies or 0),
        "successful_companies": int(row.successful_companies or 0),
        "failed_companies": int(row.failed_companies or 0),
        "jobs_new": int(row.jobs_new or 0),
        "jobs_updated": int(row.jobs_updated or 0),
        "jobs_fetched": int(row.jobs_fetched or 0),
        "schedule_metadata": row.schedule_metadata,
    }
