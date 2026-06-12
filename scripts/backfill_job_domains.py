#!/usr/bin/env python3
"""Re-queue active jobs for v5 domain enrichment and sync candidate domains."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
PROFILE_SERVICE = ROOT / "profile_service"
sys.path.insert(0, str(JOB_INGESTION))
import os

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import (
    cleanup_orphan_enrichment_queue,
    process_enrichment_window,
    queue_job_for_enrichment,
)
from app.models.normalized_job import NormalizedJob


async def count_jobs(*, target_version: str) -> dict:
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) FILTER (WHERE is_active) AS active,
                      COUNT(*) FILTER (WHERE is_active AND job_domain IS NOT NULL) AS with_domain,
                      COUNT(*) FILTER (
                        WHERE is_active AND (
                          job_domain IS NULL OR extraction_version != :target
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
                    JOIN raw_jobs rj ON rj.id = nj.raw_job_id
                    WHERE nj.is_active
                      AND nj.processing_state IN ('success', 'partial_success', 'pending')
                      AND (nj.job_domain IS NULL OR nj.extraction_version != :target)
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
                source="domain_backfill",
                priority=1,
            )
            requeued += 1
        await db.commit()
    return requeued


async def drain_queue(*, max_windows: int, target_version: str) -> int:
    from app.config import Settings

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


async def sync_all_candidate_domains() -> list[tuple[str, str | None, str | None]]:
    if str(PROFILE_SERVICE) not in sys.path:
        sys.path.insert(0, str(PROFILE_SERVICE))
    from app.domain import derive_user_domains

    results: list[tuple[str, str | None, str | None]] = []
    async with AsyncSessionLocal() as db:
        profiles = (
            await db.execute(
                text(
                    """
                    SELECT cp.candidate_id, cp.id, cp.version
                    FROM candidate_profiles cp
                    WHERE cp.is_current = true
                    """
                )
            )
        ).all()
        for candidate_id, profile_id, version in profiles:
            caps = list(
                await db.scalars(
                    text(
                        """
                        SELECT capability_name FROM candidate_capabilities
                        WHERE candidate_id = :cid AND profile_version = :ver
                        """
                    ),
                    {"cid": candidate_id, "ver": version},
                )
            )
            primary, secondary = derive_user_domains(caps)
            await db.execute(
                text(
                    """
                    UPDATE candidate_profiles
                    SET primary_domain = :primary, secondary_domain = :secondary
                    WHERE id = :pid
                    """
                ),
                {"primary": primary, "secondary": secondary, "pid": profile_id},
            )
            results.append((str(candidate_id), primary, secondary))
        await db.commit()
    return results


async def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill job domains via v5 enrichment")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--skip-requeue", action="store_true")
    parser.add_argument("--skip-drain", action="store_true")
    parser.add_argument("--skip-candidates", action="store_true")
    parser.add_argument("--reset-failed", action="store_true", help="Reset failed queue rows for jobs missing domain")
    parser.add_argument("--max-windows", type=int, default=50)
    args = parser.parse_args()

    target_version = os.environ.get("EXTRACTION_VERSION", "v5")
    before = await count_jobs(target_version=target_version)
    print(f"Before: {before}")

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
                    JOIN raw_jobs rj ON rj.id = nj.raw_job_id
                    WHERE eq.normalized_job_id = nj.id
                      AND eq.status IN ('failed', 'quota_blocked')
                      AND nj.is_active
                    """
                )
            )
            await db.commit()
            print(f"Reset {result.rowcount} failed queue rows")

    if not args.skip_requeue:
        requeued = await requeue_jobs(target_version=target_version, limit=args.limit)
        print(f"Requeued {requeued} jobs for {target_version}")

    if not args.skip_drain:
        processed = await drain_queue(max_windows=args.max_windows, target_version=target_version)
        print(f"Processed {processed} jobs in enrichment windows")

    if not args.skip_candidates:
        synced = await sync_all_candidate_domains()
        for candidate_id, primary, secondary in synced:
            print(f"Candidate {candidate_id}: {primary}" + (f" + {secondary}" if secondary else ""))

    after = await count_jobs(target_version=target_version)
    print(f"After: {after}")


if __name__ == "__main__":
    asyncio.run(main())
