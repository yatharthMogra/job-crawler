#!/usr/bin/env python3
"""Pause enrichment, backfill Ashby descriptions, and re-queue incomplete jobs."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "job_ingestion"))

from sqlalchemy import select, text

from app.database import AsyncSessionLocal
from app.ingestion.connectors.ashby import AshbyConnector
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import get_enrichment_worker, queue_job_for_enrichment
from app.ingestion.extractor.deterministic import extract_deterministic_fields
from app.ingestion.extractor.text_cleaner import clean_job_description
from app.ingestion.extractor.text_cleaner import build_description_preview
from app.ingestion.pipeline import _resolve_description_text
from app.models.company import Company
from app.models.normalized_job import NormalizedJob
from app.models.raw_job import RawJob

ASHBY_TOKENS = ("ramp", "notion", "linear")
ACTIVE_QUEUE_STATUSES = ("queued", "cooldown", "in_progress", "failed")


async def pause_enrichment_queue() -> int:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            text(
                """
                UPDATE enrichment_queue
                SET status = 'paused', next_retry_at = NULL, updated_at = NOW()
                WHERE status = ANY(:statuses)
                """
            ),
            {"statuses": list(ACTIVE_QUEUE_STATUSES)},
        )
        await db.commit()
        return int(result.rowcount or 0)


async def backfill_ashby_descriptions(board_tokens: tuple[str, ...] = ASHBY_TOKENS) -> dict[str, int]:
    connector = AshbyConnector()
    stats = {"companies": 0, "fetched": 0, "updated": 0, "missing": 0}

    async with AsyncSessionLocal() as db:
        companies = (
            await db.scalars(
                select(Company).where(
                    Company.platform == "ashby",
                    Company.board_token.in_(board_tokens),
                )
            )
        ).all()

        for company in companies:
            stats["companies"] += 1
            print(f"fetching {company.board_token}...", flush=True)
            postings = await connector.fetch_jobs(company)
            stats["fetched"] += len(postings)
            print(f"fetched {company.board_token}: {len(postings)} postings", flush=True)

            normalized_rows = (
                await db.scalars(
                    select(NormalizedJob).where(
                        NormalizedJob.company_id == company.id,
                        NormalizedJob.is_active.is_(True),
                    )
                )
            ).all()
            by_external_id = {row.external_job_id: row for row in normalized_rows}

            for posting in postings:
                fields = extract_deterministic_fields(posting, platform="ashby")
                external_id = fields["external_job_id"]
                normalized = by_external_id.get(external_id)
                if normalized is None:
                    stats["missing"] += 1
                    continue

                raw_job = await db.get(RawJob, normalized.raw_job_id)
                if raw_job is None:
                    stats["missing"] += 1
                    continue

                raw_html = fields.get("raw_html") or ""
                description_text = _resolve_description_text(posting, raw_html) or ""
                raw_job.raw_api_response = posting
                raw_job.raw_html = raw_html
                normalized.title = fields.get("title") or normalized.title
                normalized.location = fields.get("location")
                normalized.department = fields.get("department")
                normalized.posting_url = fields.get("posting_url")
                normalized.posted_at = fields.get("posted_at")
                normalized.employment_type = fields.get("employment_type")
                normalized.description_text = description_text or None
                normalized.description_preview = build_description_preview(description_text)
                stats["updated"] += 1

            await db.commit()
            print(f"backfilled {company.board_token}: updated={stats['updated']}", flush=True)
    return stats


async def requeue_incomplete_jobs() -> int:
    requeued = 0
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    """
                    SELECT nj.id
                    FROM normalized_jobs nj
                    LEFT JOIN enrichment_queue eq ON eq.normalized_job_id = nj.id
                    WHERE nj.is_active
                      AND (
                        nj.processing_state IN ('pending', 'partial_success', 'enrichment_failed')
                        OR eq.status IN ('paused', 'failed', 'cooldown')
                      )
                    ORDER BY nj.created_at
                    """
                )
            )
        ).all()

        for (job_id,) in rows:
            job = await db.get(NormalizedJob, job_id)
            if job is None:
                continue
            if job.processing_state == ProcessingState.SUCCESS:
                continue
            job.processing_state = ProcessingState.PENDING
            job.failure_reason = None
            job.last_failure_at = None
            await queue_job_for_enrichment(
                db=db,
                normalized_job_id=job_id,
                pipeline_run_id=None,
                source="ashby_backfill_requeue",
                priority=0,
            )
            requeued += 1

        await db.execute(
            text(
                """
                UPDATE enrichment_queue
                SET status = 'queued',
                    attempt_count = 0,
                    next_retry_at = NULL,
                    last_error = NULL,
                    last_failure_reason = NULL,
                    updated_at = NOW()
                WHERE status IN ('paused', 'failed', 'cooldown')
                """
            )
        )
        await db.commit()
    get_enrichment_worker().wake()
    return requeued


async def queue_snapshot() -> dict:
    async with AsyncSessionLocal() as db:
        queue = (
            await db.execute(
                text("SELECT status, COUNT(*) FROM enrichment_queue GROUP BY status ORDER BY 2 DESC")
            )
        ).all()
        states = (
            await db.execute(
                text(
                    """
                    SELECT processing_state, COUNT(*)
                    FROM normalized_jobs
                    WHERE is_active
                    GROUP BY processing_state
                    ORDER BY 2 DESC
                    """
                )
            )
        ).all()
        ashby_html = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE length(rj.raw_html) > 100) AS with_desc,
                      COUNT(*) AS total
                    FROM normalized_jobs nj
                    JOIN raw_jobs rj ON rj.id = nj.raw_job_id
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.platform = 'ashby' AND nj.is_active
                    """
                )
            )
        ).one()
        return {
            "queue": dict(queue),
            "processing_state": dict(states),
            "ashby_with_description": dict(ashby_html._mapping),
        }


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-pause", action="store_true")
    parser.add_argument("--skip-backfill", action="store_true")
    parser.add_argument("--skip-requeue", action="store_true")
    parser.add_argument("--ashby-token", action="append", dest="ashby_tokens")
    args = parser.parse_args()
    tokens = tuple(args.ashby_tokens) if args.ashby_tokens else ASHBY_TOKENS

    if not args.skip_pause:
        paused = await pause_enrichment_queue()
        print(f"paused_queue_rows={paused}")

    if not args.skip_backfill:
        backfill = await backfill_ashby_descriptions(tokens)
        print(f"backfill={json.dumps(backfill)}")

    if not args.skip_requeue:
        requeued = await requeue_incomplete_jobs()
        print(f"requeued={requeued}")

    snapshot = await queue_snapshot()
    print(f"snapshot={json.dumps(snapshot, default=str)}")


if __name__ == "__main__":
    asyncio.run(main())
