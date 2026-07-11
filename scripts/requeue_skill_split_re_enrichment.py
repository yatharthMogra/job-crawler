#!/usr/bin/env python3
"""Re-queue jobs for batched required/preferred skill split re-enrichment.

Run with job_ingestion up; the in-process enrichment worker pool drains the queue.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

os.chdir(JOB_INGESTION)

from sqlalchemy import text  # noqa: E402

from app.config import Settings  # noqa: E402
from app.database import AsyncSessionLocal  # noqa: E402
from app.ingestion.constants import ProcessingState  # noqa: E402
from app.ingestion.enrichment_worker import (  # noqa: E402
    get_enrichment_worker,
    queue_job_for_enrichment,
)
from app.models.normalized_job import NormalizedJob  # noqa: E402


async def count_candidates(target_version: str, *, active_only: bool) -> dict:
    active_clause = "AND is_active" if active_only else ""
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    f"""
                    SELECT
                      COUNT(*) AS candidates,
                      COUNT(*) FILTER (WHERE extraction_version = :target) AS already_target,
                      COUNT(*) FILTER (WHERE extraction_version != :target) AS needs_reenrich
                    FROM normalized_jobs
                    WHERE processing_state IN ('success', 'partial_success', 'pending')
                      {active_clause}
                    """
                ),
                {"target": target_version},
            )
        ).one()
        return dict(row._mapping)


async def requeue_jobs(
    *,
    target_version: str,
    source: str,
    limit: int | None,
    active_only: bool,
) -> int:
    active_clause = "AND is_active" if active_only else ""
    limit_clause = f"LIMIT {int(limit)}" if limit else ""
    requeued = 0
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    f"""
                    SELECT id FROM normalized_jobs
                    WHERE processing_state IN ('success', 'partial_success', 'pending')
                      AND extraction_version != :target
                      {active_clause}
                    ORDER BY created_at
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
                source=source,
                priority=1,
            )
            requeued += 1
        await db.commit()
    return requeued


async def _stats() -> dict:
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active AND extraction_version = :target) AS target_jobs,
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active AND extraction_version != :target) AS legacy_jobs,
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active
                         AND cardinality(required_skills) = 0
                         AND cardinality(required_qualifications) > 0) AS missing_required_skills,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'queued') AS queued,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'in_progress') AS in_progress,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'cooldown') AS cooldown
                    """
                ),
                {"target": Settings().extraction_version},
            )
        ).one()
        return dict(row._mapping)


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-version", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--include-inactive", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    settings = Settings()
    target_version = args.target_version or settings.extraction_version
    print(
        json.dumps(
            {
                "target_version": target_version,
                "extraction_version_env": settings.extraction_version,
                "workers": settings.resolved_enrichment_worker_count(),
            }
        ),
        flush=True,
    )

    counts = await count_candidates(target_version, active_only=not args.include_inactive)
    print(json.dumps({"event": "candidates", **counts}), flush=True)
    if args.dry_run:
        return

    requeued = await requeue_jobs(
        target_version=target_version,
        source="skill_split_requeue",
        limit=args.limit,
        active_only=not args.include_inactive,
    )
    get_enrichment_worker().wake()
    print(json.dumps({"event": "requeued", "count": requeued}), flush=True)
    print(json.dumps({"event": "stats", **await _stats()}), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
