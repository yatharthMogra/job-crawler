#!/usr/bin/env python3
"""Re-queue jobs that failed enrichment due to token/rate limits.

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

from sqlalchemy import text

from app.config import Settings
from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import get_enrichment_worker, queue_job_for_enrichment
from app.models.normalized_job import NormalizedJob

TOKEN_FAILURE_REASONS = (
    "token_limit_exceeded",
    "retry_limit_exceeded",
)


async def _candidate_job_ids(
    *,
    board_tokens: list[str] | None,
    target_version: str,
) -> list[UUID]:
    company_filter = ""
    params: dict = {"target": target_version}
    if board_tokens:
        company_filter = "AND c.board_token = ANY(:tokens)"
        params["tokens"] = board_tokens

    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    f"""
                    SELECT DISTINCT nj.id
                    FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    LEFT JOIN enrichment_queue eq ON eq.normalized_job_id = nj.id
                    WHERE nj.is_active
                      AND nj.processing_state IN ('success', 'partial_success', 'pending')
                      {company_filter}
                      AND (
                        nj.extraction_version != :target
                        OR eq.last_failure_reason = ANY(:reasons)
                        OR (
                          eq.status IN ('failed', 'cooldown')
                          AND (
                            eq.last_error ILIKE '%429%'
                            OR eq.last_error ILIKE '%quota%'
                            OR eq.last_error ILIKE '%RESOURCE_EXHAUSTED%'
                          )
                        )
                      )
                    ORDER BY nj.id
                    """
                ),
                {
                    **params,
                    "reasons": list(TOKEN_FAILURE_REASONS),
                },
            )
        ).all()
        return [UUID(str(row[0])) for row in rows]


async def requeue_candidates(job_ids: list[UUID], *, source: str) -> int:
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
                priority=2,
            )
            requeued += 1
        await db.commit()
    return requeued


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board-tokens", default="", help="Comma-separated company board tokens")
    parser.add_argument("--target-version", default="v3")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    board_tokens = [t.strip() for t in args.board_tokens.split(",") if t.strip()] or None
    settings = Settings()
    print(
        json.dumps(
            {
                "model": settings.gemini_model,
                "micro_batch_size": settings.enrichment_micro_batch_size,
                "max_batches_per_window": settings.enrichment_max_batches_per_window,
                "max_jobs_per_window": settings.enrichment_max_jobs_per_window,
                "llm_max_rpm": settings.enrichment_llm_max_rpm,
                "workers": settings.resolved_enrichment_worker_count(),
            }
        ),
        flush=True,
    )

    job_ids = await _candidate_job_ids(
        board_tokens=board_tokens,
        target_version=args.target_version,
    )
    print(json.dumps({"event": "candidates", "count": len(job_ids), "board_tokens": board_tokens}), flush=True)
    if args.dry_run:
        return

    requeued = await requeue_candidates(job_ids, source="token_limit_requeue")
    get_enrichment_worker().wake()
    print(json.dumps({"event": "requeued", "count": requeued}), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
