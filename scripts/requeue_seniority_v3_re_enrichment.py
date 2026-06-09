#!/usr/bin/env python3
"""Re-queue jobs for batched seniority v3 LLM re-enrichment and drain the queue."""

from __future__ import annotations

import argparse
import asyncio
import json
import socket
import sys
import time
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))
import os

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.config import Settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import (
    process_enrichment_window,
    queue_job_for_enrichment,
)
from app.models.normalized_job import NormalizedJob


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


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
                       WHERE is_active AND extraction_version = 'v3') AS v3_jobs,
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active AND extraction_version != 'v3') AS legacy_jobs,
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active AND is_internship) AS internships,
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active AND is_new_grad) AS new_grads,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'queued') AS queued,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'in_progress') AS in_progress,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'cooldown') AS cooldown,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'failed') AS failed
                    """
                )
            )
        ).one()
        seniority = await db.execute(
            text(
                """
                SELECT seniority, COUNT(*) AS jobs
                FROM normalized_jobs
                WHERE is_active
                GROUP BY seniority
                ORDER BY jobs DESC
                LIMIT 12
                """
            )
        )
        pools = await db.execute(
            text(
                """
                SELECT pool, COUNT(*) AS jobs
                FROM (
                    SELECT unnest(retrieval_pools) AS pool
                    FROM normalized_jobs
                    WHERE is_active
                ) sub
                WHERE pool LIKE '%INTERNSHIP%' OR pool LIKE '%NEW_GRAD%'
                GROUP BY pool
                ORDER BY jobs DESC
                LIMIT 8
                """
            )
        )
        payload = dict(row._mapping)
        payload["seniority_top"] = [dict(r._mapping) for r in seniority]
        payload["intern_newgrad_pools"] = [dict(r._mapping) for r in pools]
        return payload


async def run_worker_until_drained(
    settings: Settings,
    *,
    timeout_s: int,
    poll_s: float,
) -> dict:
    start = time.monotonic()
    last: dict | None = None
    idle_rounds = 0

    while time.monotonic() - start < timeout_s:
        processed = 0
        batches = 0
        try:
            async with AsyncSessionLocal() as db:
                processed, batches = await process_enrichment_window(db=db, settings=settings)
        except Exception as exc:
            if "deadlock" in str(exc).lower():
                print(json.dumps({"event": "deadlock_retry", "message": str(exc)[:200]}), flush=True)
                await asyncio.sleep(2)
                continue
            raise

        row = await _stats()
        if row != last:
            print(json.dumps({"event": "progress", **row, "last_window_jobs": processed, "last_window_batches": batches}, default=str), flush=True)
            last = row

        if processed == 0:
            idle_rounds += 1
        else:
            idle_rounds = 0

        if row["queued"] == 0 and row["in_progress"] == 0 and row["cooldown"] == 0:
            return row

        if processed > 0:
            await asyncio.sleep(settings.enrichment_window_seconds)
        elif row["cooldown"] > 0:
            await asyncio.sleep(max(poll_s, settings.enrichment_cooldown_seconds / 4))
        else:
            await asyncio.sleep(poll_s)

        if idle_rounds >= 3 and row["queued"] == 0 and row["in_progress"] == 0:
            return row

    raise TimeoutError(f"Re-enrichment timed out: {last}")


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-version", default="v3")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--include-inactive", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--drain-only", action="store_true", help="Process existing queue without re-enqueueing")
    parser.add_argument("--queue-only", action="store_true", help="Only enqueue; rely on running job_ingestion worker")
    parser.add_argument("--timeout-s", type=int, default=7200)
    args = parser.parse_args()

    settings = Settings()
    print(
        json.dumps(
            {
                "target_version": args.target_version,
                "extraction_version_env": settings.extraction_version,
                "micro_batch_size": settings.enrichment_micro_batch_size,
                "max_tokens_per_batch": settings.enrichment_max_input_tokens_per_batch,
                "window_token_budget": settings.enrichment_window_token_budget,
                "max_jobs_per_window": settings.enrichment_max_jobs_per_window,
            }
        ),
        flush=True,
    )

    counts = await count_candidates(args.target_version, active_only=not args.include_inactive)
    print(json.dumps({"event": "candidates", **counts}), flush=True)
    if args.dry_run:
        return

    if not args.drain_only and not args.queue_only and _port_open("127.0.0.1", 8000):
        print(
            json.dumps(
                {
                    "warning": "job_ingestion appears to be running on :8000; "
                    "use --queue-only to avoid duplicate workers, or stop the service first",
                }
            ),
            flush=True,
        )
        print("Aborting inline worker to prevent duplicate batch processing.", flush=True)
        args.queue_only = True

    if not args.drain_only:
        requeued = await requeue_jobs(
            target_version=args.target_version,
            source="seniority_v3_requeue",
            limit=args.limit,
            active_only=not args.include_inactive,
        )
        print(json.dumps({"event": "requeued", "count": requeued}), flush=True)
        if requeued == 0 and not args.queue_only:
            final = await _stats()
            print(json.dumps({"event": "done", **final}, default=str), flush=True)
            return

    if args.queue_only:
        print(
            json.dumps(
                {
                    "event": "queued",
                    "message": "Jobs queued; ensure job_ingestion service is running with EXTRACTION_VERSION=v3",
                }
            ),
            flush=True,
        )
        return

    final = await run_worker_until_drained(settings, timeout_s=args.timeout_s, poll_s=5.0)
    print(json.dumps({"event": "done", **final}, default=str), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
