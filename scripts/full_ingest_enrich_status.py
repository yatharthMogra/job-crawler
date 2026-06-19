#!/usr/bin/env python3
"""Status report for ingest + enrichment (job_ingestion service)."""

from __future__ import annotations

import asyncio
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

from sqlalchemy import text

from app.database import AsyncSessionLocal


def _service_running() -> bool:
    try:
        out = subprocess.check_output(
            ["pgrep", "-fl", "uvicorn"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return False
    return "app.main:app" in out or "job_ingestion" in out


def _pipeline_running() -> bool:
    try:
        out = subprocess.check_output(["pgrep", "-fl", "run_pipeline"], text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    return "run_pipeline" in out or "app.ingestion.pipeline" in out


async def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"=== Ingest + enrich status @ {now} ===")

    pipeline = _pipeline_running()
    service = _service_running()
    print(f"pipeline_running={pipeline} job_ingestion_service={service}")

    async with AsyncSessionLocal() as db:
        companies = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE is_active) AS active,
                      COUNT(*) AS total,
                      COUNT(*) FILTER (
                        WHERE is_active AND EXISTS (
                          SELECT 1 FROM normalized_jobs nj
                          WHERE nj.company_id = companies.id AND nj.is_active
                        )
                      ) AS with_jobs,
                      COUNT(*) FILTER (
                        WHERE is_active AND NOT EXISTS (
                          SELECT 1 FROM normalized_jobs nj
                          WHERE nj.company_id = companies.id AND nj.is_active
                        )
                      ) AS without_jobs
                    FROM companies
                    """
                )
            )
        ).one()
        jobs = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE is_active) AS active,
                      COUNT(*) FILTER (WHERE is_active AND processing_state = 'success') AS enriched,
                      COUNT(*) FILTER (WHERE is_active AND processing_state = 'pending') AS pending,
                      COUNT(*) FILTER (WHERE is_active AND job_domain IS NOT NULL) AS with_domain,
                      COUNT(*) FILTER (WHERE is_active AND extraction_version = 'v5') AS on_v5,
                      COUNT(*) FILTER (WHERE is_active AND role_intent IS NOT NULL) AS with_role_intent,
                      COUNT(*) FILTER (WHERE is_active AND requires_clearance) AS requires_clearance,
                      COUNT(*) FILTER (WHERE is_active AND extraction_version = 'v6') AS on_v6
                    FROM normalized_jobs
                    """
                )
            )
        ).one()
        queue = (
            await db.execute(
                text(
                    """
                    SELECT status, COALESCE(last_failure_reason, ''), COUNT(*)::int
                    FROM enrichment_queue
                    GROUP BY 1, 2
                    ORDER BY 3 DESC
                    """
                )
            )
        ).all()
        completed_5m = await db.scalar(
            text(
                """
                SELECT COUNT(*)::int FROM enrichment_queue
                WHERE status = 'completed'
                  AND updated_at > NOW() - INTERVAL '5 minutes'
                """
            )
        )
        queued = await db.scalar(
            text(
                """
                SELECT COUNT(*)::int FROM enrichment_queue
                WHERE status IN ('queued', 'cooldown', 'in_progress')
                """
            )
        )
        latest_run = (
            await db.execute(
                text(
                    """
                    SELECT status, total_companies, successful_companies, failed_companies,
                           jobs_new, jobs_updated, started_at
                    FROM pipeline_runs
                    ORDER BY started_at DESC
                    LIMIT 1
                    """
                )
            )
        ).first()

    active, total, with_jobs, without_jobs = companies
    active_jobs, enriched, pending, with_domain, on_v5, with_role_intent, requires_clearance, on_v6 = jobs
    pct = 100 * with_domain / active_jobs if active_jobs else 0
    role_intent_pct = 100 * with_role_intent / active_jobs if active_jobs else 0
    v6_pct = 100 * on_v6 / active_jobs if active_jobs else 0
    enrich_pct = 100 * enriched / active_jobs if active_jobs else 0

    print(
        f"companies: active={active}/{total} with_jobs={with_jobs} "
        f"awaiting_first_fetch={without_jobs}"
    )
    print(
        f"jobs: active={active_jobs} enriched={enriched} ({enrich_pct:.1f}%) "
        f"pending={pending} domain={with_domain} ({pct:.1f}%) v5={on_v5} "
        f"role_intent={with_role_intent} ({role_intent_pct:.1f}%) "
        f"requires_clearance={requires_clearance} v6={on_v6} ({v6_pct:.1f}%)"
    )
    print(f"queue_pending={queued} completed_last_5min={completed_5m}")
    print("queue_breakdown:")
    for status, reason, count in queue:
        print(f"  {status:16} {reason:32} {count}")
    if latest_run:
        print(
            "latest_pipeline_run: "
            f"status={latest_run.status} companies={latest_run.successful_companies}/"
            f"{latest_run.total_companies} failed={latest_run.failed_companies} "
            f"new={latest_run.jobs_new} updated={latest_run.jobs_updated} "
            f"started={latest_run.started_at}"
        )


if __name__ == "__main__":
    asyncio.run(main())
