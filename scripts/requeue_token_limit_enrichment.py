#!/usr/bin/env python3
"""Re-queue jobs that failed enrichment due to token/rate limits and drain with batched LLM."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
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
from app.ingestion.enrichment_worker import process_enrichment_window, queue_job_for_enrichment
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


async def _stats(board_tokens: list[str] | None) -> dict:
    company_filter = ""
    params: dict = {}
    if board_tokens:
        company_filter = "AND c.board_token = ANY(:tokens)"
        params["tokens"] = board_tokens

    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    f"""
                    SELECT
                      (SELECT COUNT(*) FROM normalized_jobs nj
                       JOIN companies c ON c.id = nj.company_id
                       WHERE nj.is_active AND nj.extraction_version = 'v3' {company_filter}) AS v3_jobs,
                      (SELECT COUNT(*) FROM normalized_jobs nj
                       JOIN companies c ON c.id = nj.company_id
                       WHERE nj.is_active AND nj.extraction_version != 'v3' {company_filter}) AS legacy_jobs,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'queued') AS queued,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'in_progress') AS in_progress,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'cooldown') AS cooldown,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'failed') AS failed
                    """
                ),
                params,
            )
        ).one()
        return dict(row._mapping)


async def run_worker_until_drained(settings: Settings, *, timeout_s: int) -> dict:
    start = time.monotonic()
    last: dict | None = None
    while time.monotonic() - start < timeout_s:
        processed = 0
        batches = 0
        try:
            async with AsyncSessionLocal() as db:
                processed, batches = await process_enrichment_window(db=db, settings=settings)
        except Exception as exc:
            if "deadlock" in str(exc).lower():
                print(json.dumps({"event": "deadlock_retry"}), flush=True)
                await asyncio.sleep(2)
                continue
            raise

        row = await _stats(board_tokens=None)
        if row != last:
            print(
                json.dumps(
                    {
                        "event": "progress",
                        **row,
                        "last_window_jobs": processed,
                        "last_window_batches": batches,
                    },
                    default=str,
                ),
                flush=True,
            )
            last = row

        if row["queued"] == 0 and row["in_progress"] == 0 and row["cooldown"] == 0:
            return row

        if processed > 0:
            await asyncio.sleep(settings.enrichment_window_seconds)
        else:
            await asyncio.sleep(5)

    raise TimeoutError(f"Drain timed out: {last}")


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board-tokens", default="", help="Comma-separated company board tokens")
    parser.add_argument("--target-version", default="v3")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--queue-only", action="store_true")
    parser.add_argument("--timeout-s", type=int, default=7200)
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
                "batch_interval_seconds": settings.enrichment_batch_interval_seconds,
                "token_estimation": settings.enrichment_token_estimation_strategy,
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
    print(json.dumps({"event": "requeued", "count": requeued}), flush=True)
    if requeued == 0 or args.queue_only:
        return

    final = await run_worker_until_drained(settings, timeout_s=args.timeout_s)
    print(json.dumps({"event": "done", **final}, default=str), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
