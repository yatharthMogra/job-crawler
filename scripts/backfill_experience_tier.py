#!/usr/bin/env python3
"""Re-queue active jobs for v8 experience_tier enrichment."""

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

from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import (
    cleanup_orphan_enrichment_queue,
    get_enrichment_worker,
    queue_job_for_enrichment,
    reset_stuck_queue_rows,
)
from app.models.normalized_job import NormalizedJob

TARGET_VERSION = os.environ.get("EXTRACTION_VERSION", "v8")


async def count_jobs(*, target_version: str) -> dict:
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE is_active) AS active,
                      COUNT(*) FILTER (WHERE is_active AND experience_tier != 'UNKNOWN') AS with_tier,
                      COUNT(*) FILTER (WHERE is_active AND extraction_version = :target) AS on_target,
                      COUNT(*) FILTER (
                        WHERE is_active AND (
                          experience_tier = 'UNKNOWN' OR extraction_version != :target
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
                      AND (nj.experience_tier = 'UNKNOWN' OR nj.extraction_version != :target)
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
            await queue_job_for_enrichment(db, job, source="experience_tier_backfill")
            requeued += 1
        await db.commit()
    return requeued


async def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill experience_tier via enrichment re-queue")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    stats = await count_jobs(target_version=TARGET_VERSION)
    print(f"Target extraction_version={TARGET_VERSION}")
    print(f"Active jobs: {stats['active']}")
    print(f"With experience_tier set: {stats['with_tier']}")
    print(f"On target version: {stats['on_target']}")
    print(f"Needs re-enrichment: {stats['needs_reenrich']}")

    if args.dry_run:
        print("Dry run — no jobs re-queued.")
        return

    await reset_stuck_queue_rows()
    await cleanup_orphan_enrichment_queue()
    worker = get_enrichment_worker()
    if worker is None:
        print("Warning: enrichment worker pool not running in this process.")
        print("Start job_ingestion service so workers drain the queue.")

    requeued = await requeue_jobs(target_version=TARGET_VERSION, limit=args.limit)
    print(f"Re-queued {requeued} jobs.")


if __name__ == "__main__":
    asyncio.run(main())
