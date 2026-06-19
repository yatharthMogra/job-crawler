#!/usr/bin/env python3
"""Re-queue jobs for batched taxonomy v4 LLM re-enrichment.

Run with job_ingestion up; the in-process enrichment worker pool drains the queue.
"""

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
from app.ingestion.enrichment_worker import get_enrichment_worker, queue_job_for_enrichment
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
                       WHERE is_active AND extraction_version = 'v4') AS v4_jobs,
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active AND extraction_version != 'v4') AS legacy_jobs,
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


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-version", default="v4")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--include-inactive", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    settings = Settings()
    print(
        json.dumps(
            {
                "target_version": args.target_version,
                "extraction_version_env": settings.extraction_version,
                "workers": settings.resolved_enrichment_worker_count(),
            }
        ),
        flush=True,
    )

    counts = await count_candidates(args.target_version, active_only=not args.include_inactive)
    print(json.dumps({"event": "candidates", **counts}), flush=True)
    if args.dry_run:
        return

    requeued = await requeue_jobs(
        target_version=args.target_version,
        source="seniority_v4_requeue",
        limit=args.limit,
        active_only=not args.include_inactive,
    )
    get_enrichment_worker().wake()
    print(json.dumps({"event": "requeued", "count": requeued}), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
