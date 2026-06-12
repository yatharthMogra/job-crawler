#!/usr/bin/env python3
"""Re-queue jobs for targeted domain/pool enrichment fixes (presets 2a, 2b, 2c)."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

import os

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import process_enrichment_window, queue_job_for_enrichment
from app.models.normalized_job import NormalizedJob

PRESET_QUERIES = {
    "2a": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.processing_state = 'success'
          AND (
            ('HARDWARE_ENGINEER' = ANY(nj.normalized_roles)
             AND nj.job_domain NOT IN ('Hardware_Electrical', 'Aerospace_Defense'))
            OR
            ('OPERATIONS' = ANY(nj.normalized_roles) AND nj.job_domain = 'Software')
          )
    """,
    "2b": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Research_Science'
          AND (nj.retrieval_pools IS NULL OR cardinality(nj.retrieval_pools) = 0)
          AND nj.processing_state = 'success'
    """,
    "2c": """
        SELECT nj.id FROM normalized_jobs nj
        JOIN companies c ON c.id = nj.company_id
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Aerospace_Defense'
          AND 'SWE' = ANY(nj.normalized_roles)
          AND (nj.retrieval_pools IS NULL OR cardinality(nj.retrieval_pools) = 0)
          AND nj.processing_state = 'success'
          AND c.platform IN ('workday', 'oracle_hcm')
    """,
}


async def collect_job_ids(presets: list[str]) -> list[UUID]:
    ids: set[UUID] = set()
    async with AsyncSessionLocal() as db:
        for preset in presets:
            query = PRESET_QUERIES[preset]
            rows = (await db.execute(text(query))).all()
            for (job_id,) in rows:
                ids.add(UUID(str(job_id)))
            print(f"preset {preset}: {len(rows)} jobs")
    return sorted(ids)


async def requeue(job_ids: list[UUID], source: str) -> int:
    requeued = 0
    async with AsyncSessionLocal() as db:
        for job_id in job_ids:
            job = await db.get(NormalizedJob, job_id)
            if job is None:
                continue
            job.processing_state = ProcessingState.PENDING
            job.failure_reason = None
            job.last_failure_at = None
            await queue_job_for_enrichment(
                db=db,
                normalized_job_id=job_id,
                pipeline_run_id=None,
                source=source,
                priority=1,
            )
            requeued += 1
        await db.commit()
    return requeued


async def drain(max_windows: int) -> int:
    settings = get_settings()
    processed = 0
    for _ in range(max_windows):
        async with AsyncSessionLocal() as db:
            count, _ = await process_enrichment_window(db, settings=settings)
            await db.commit()
        if count == 0:
            break
        processed += count
    return processed


async def main() -> None:
    parser = argparse.ArgumentParser(description="Re-queue jobs for domain fix presets")
    parser.add_argument("--preset", choices=["2a", "2b", "2c"], action="append")
    parser.add_argument("--all", action="store_true", help="Run all presets 2a, 2b, 2c")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--drain",
        action="store_true",
        help="Drain enrichment queue after requeue (prefer: parallel_gemini_drain_today.py --launch-all)",
    )
    parser.add_argument("--max-windows", type=int, default=500)
    args = parser.parse_args()

    presets = args.preset or (["2a", "2b", "2c"] if args.all else [])
    if not presets:
        parser.error("Specify --preset or --all")

    job_ids = await collect_job_ids(presets)
    print(f"unique jobs to requeue: {len(job_ids)}")
    if args.dry_run:
        return

    source = "domain_fix_" + "_".join(presets)
    requeued = await requeue(job_ids, source=source)
    print(f"requeued {requeued} jobs")

    if args.drain:
        processed = await drain(args.max_windows)
        print(f"drained {processed} jobs via enrichment worker")


if __name__ == "__main__":
    asyncio.run(main())
