#!/usr/bin/env python3
"""Re-queue jobs with empty tech_stack/skills for batched LLM re-enrichment."""

from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "job_ingestion"))

from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import get_enrichment_worker, queue_job_for_enrichment
from app.models.normalized_job import NormalizedJob


async def requeue_empty_skill_jobs() -> int:
    requeued = 0
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    """
                    SELECT id FROM normalized_jobs
                    WHERE processing_state IN ('success', 'partial_success', 'pending')
                      AND cardinality(tech_stack) = 0
                      AND cardinality(skills) = 0
                    ORDER BY created_at
                    """
                )
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
                normalized_job_id=job_id,
                pipeline_run_id=None,
                source="skill_extraction_requeue",
                priority=1,
            )
            requeued += 1
        await db.commit()
    get_enrichment_worker().wake()
    return requeued


async def _stats() -> dict:
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active
                         AND (cardinality(tech_stack) > 0 OR cardinality(skills) > 0)) AS with_skills,
                      (SELECT COUNT(*) FROM normalized_jobs
                       WHERE is_active
                         AND cardinality(tech_stack) = 0
                         AND cardinality(skills) = 0
                         AND processing_state = 'success') AS still_empty_success,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'queued') AS queued,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'in_progress') AS in_progress,
                      (SELECT COUNT(*) FROM enrichment_queue WHERE status = 'cooldown') AS cooldown
                    """
                )
            )
        ).one()
        return dict(row._mapping)


async def wait_for_drain(timeout_s: int = 7200) -> dict:
    start = time.monotonic()
    last: dict | None = None
    while time.monotonic() - start < timeout_s:
        row = await _stats()
        if row != last:
            print(json.dumps(row, default=str), flush=True)
            last = row
        if row["queued"] == 0 and row["in_progress"] == 0 and row["cooldown"] == 0:
            return row
        await asyncio.sleep(15)
    raise TimeoutError(f"Re-enrichment timed out: {last}")


async def main() -> None:
    for pass_num in range(1, 4):
        count = await requeue_empty_skill_jobs()
        print(f"pass={pass_num} requeued={count}", flush=True)
        if count == 0:
            break
        row = await wait_for_drain()
        print(f"pass={pass_num} drained:", json.dumps(row, default=str), flush=True)
        if row["still_empty_success"] == 0:
            break
    final = await _stats()
    print("done:", json.dumps(final, default=str), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
