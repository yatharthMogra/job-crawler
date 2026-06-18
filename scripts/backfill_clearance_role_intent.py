#!/usr/bin/env python3
"""Re-queue active jobs for v6 clearance + role_intent enrichment."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))
os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.config import Settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import (
    cleanup_orphan_enrichment_queue,
    process_enrichment_window,
    queue_job_for_enrichment,
)
from app.models.normalized_job import NormalizedJob

TARGET_VERSION = os.environ.get("EXTRACTION_VERSION", "v6")


async def count_jobs(*, target_version: str) -> dict:
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE is_active) AS active,
                      COUNT(*) FILTER (WHERE is_active AND role_intent IS NOT NULL) AS with_role_intent,
                      COUNT(*) FILTER (WHERE is_active AND requires_clearance) AS requires_clearance,
                      COUNT(*) FILTER (WHERE is_active AND extraction_version = :target) AS on_target,
                      COUNT(*) FILTER (
                        WHERE is_active AND (
                          role_intent IS NULL OR extraction_version != :target
                        )
                      ) AS needs_reenrich
                    FROM normalized_jobs
                    WHERE processing_state IN ('success', 'partial_success', 'pending')
                    """
                ),
                {"target": target_version},
            )
        ).one()
        return dict(row._mapping)


async def requeue_jobs(*, target_version: str, limit: int | None) -> int:
    limit_clause = f"LIMIT {int(limit)}" if limit else ""
    requeued = 0
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    f"""
                    SELECT nj.id FROM normalized_jobs nj
                    WHERE nj.is_active
                      AND nj.processing_state IN ('success', 'partial_success', 'pending')
                      AND (nj.role_intent IS NULL OR nj.extraction_version != :target)
                    ORDER BY nj.created_at
                    {limit_clause}
                    """
                ),
                {"target": target_version},
            )
        ).all()
        for (job_id,) in rows:
            job = await db.get(NormalizedJob, job_id)
            if job is None:
                continue
            job.processing_state = ProcessingState.PENDING
            job.failure_reason = None
            job.last_failure_at = None
            await queue_job_for_enrichment(
                db=db,
                normalized_job_id=UUID(str(job_id)),
                pipeline_run_id=None,
                source="clearance_role_intent_backfill",
                priority=1,
            )
            requeued += 1
        await db.commit()
    return requeued


async def drain_queue(*, max_windows: int, target_version: str) -> int:
    settings = Settings(extraction_version=target_version)
    processed = 0
    idle_rounds = 0
    for _ in range(max_windows):
        async with AsyncSessionLocal() as db:
            window_processed, _ = await process_enrichment_window(db=db, settings=settings)
        if window_processed == 0:
            idle_rounds += 1
            if idle_rounds >= 3:
                break
            await asyncio.sleep(2)
            continue
        idle_rounds = 0
        processed += window_processed
        await asyncio.sleep(settings.enrichment_window_seconds)
    return processed


async def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill requires_clearance + role_intent via v6")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--skip-requeue", action="store_true")
    parser.add_argument("--skip-drain", action="store_true")
    parser.add_argument("--reset-failed", action="store_true")
    parser.add_argument("--max-windows", type=int, default=50)
    args = parser.parse_args()

    before = await count_jobs(target_version=TARGET_VERSION)
    print(f"Before ({TARGET_VERSION}): {before}")
    if before["active"]:
        pct = 100 * before["with_role_intent"] / before["active"]
        print(f"role_intent coverage: {pct:.1f}%")

    if args.dry_run:
        print("Dry run — no changes made.")
        return

    if args.reset_failed:
        async with AsyncSessionLocal() as db:
            cleanup = await cleanup_orphan_enrichment_queue(db)
            print(f"Orphan cleanup: {cleanup}")
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                text(
                    """
                    UPDATE enrichment_queue eq
                    SET status = 'queued',
                        attempt_count = 0,
                        next_retry_at = NULL,
                        last_error = NULL,
                        last_failure_reason = NULL
                    FROM normalized_jobs nj
                    WHERE eq.normalized_job_id = nj.id
                      AND eq.status IN ('failed', 'quota_blocked')
                      AND nj.is_active
                    """
                )
            )
            await db.commit()
            print(f"Reset {result.rowcount} failed queue rows")

    if not args.skip_requeue:
        requeued = await requeue_jobs(target_version=TARGET_VERSION, limit=args.limit)
        print(f"Requeued {requeued} jobs for {TARGET_VERSION}")

    if not args.skip_drain:
        processed = await drain_queue(max_windows=args.max_windows, target_version=TARGET_VERSION)
        print(f"Processed {processed} jobs in enrichment windows")

    after = await count_jobs(target_version=TARGET_VERSION)
    print(f"After ({TARGET_VERSION}): {after}")
    if after["active"]:
        pct = 100 * after["with_role_intent"] / after["active"]
        print(f"role_intent coverage: {pct:.1f}%")


if __name__ == "__main__":
    asyncio.run(main())
