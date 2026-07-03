#!/usr/bin/env python3
"""Re-queue jobs stuck after Gemini quota errors were mislabeled as llm_schema_mismatch.

Targets enrichment_queue rows where status=failed but last_error is a 429/quota message,
and resets matching normalized_jobs back to pending for re-enrichment.

Run after deploying the enrichment_worker quota error-handling fix. Safe to dry-run first.
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
from app.ingestion.enrichment_worker import get_enrichment_worker

TARGETS_SQL = """
SELECT eq.normalized_job_id
FROM enrichment_queue eq
JOIN normalized_jobs nj ON nj.id = eq.normalized_job_id
WHERE nj.is_active
  AND eq.status = 'failed'
  AND eq.last_failure_reason = 'llm_schema_mismatch'
  AND (
    eq.last_error ILIKE '%429%'
    OR eq.last_error ILIKE '%resource_exhausted%'
    OR eq.last_error ILIKE '%quota%'
  )
ORDER BY eq.normalized_job_id
"""


async def _load_target_ids() -> list[UUID]:
    async with AsyncSessionLocal() as db:
        rows = (await db.execute(text(TARGETS_SQL))).all()
    return [UUID(str(row[0])) for row in rows]


async def requeue(job_ids: list[UUID], *, dry_run: bool) -> dict[str, int]:
    if not job_ids:
        return {"queue_reset": 0, "jobs_reset": 0}

    async with AsyncSessionLocal() as db:
        queue_result = await db.execute(
            text(
                """
                UPDATE enrichment_queue
                SET status = 'queued',
                    attempt_count = 0,
                    next_retry_at = NULL,
                    last_failure_reason = NULL,
                    last_error = NULL
                WHERE normalized_job_id = ANY(:job_ids)
                  AND status = 'failed'
                """
            ),
            {"job_ids": job_ids},
        )
        queue_reset = int(queue_result.rowcount or 0)

        job_result = await db.execute(
            text(
                """
                UPDATE normalized_jobs
                SET processing_state = 'pending',
                    failure_reason = NULL,
                    last_failure_at = NULL
                WHERE id = ANY(:job_ids)
                  AND is_active
                  AND processing_state = 'partial_success'
                  AND failure_reason = 'llm_schema_mismatch'
                """
            ),
            {"job_ids": job_ids},
        )
        jobs_reset = int(job_result.rowcount or 0)

        if dry_run:
            await db.rollback()
        else:
            await db.commit()
    return {"queue_reset": queue_reset, "jobs_reset": jobs_reset}


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview counts without writing")
    args = parser.parse_args()

    settings = Settings()
    job_ids = await _load_target_ids()
    print(
        json.dumps(
            {
                "event": "candidates",
                "dry_run": args.dry_run,
                "target_jobs": len(job_ids),
                "workers": settings.resolved_enrichment_worker_count(),
                "llm_max_rpm": settings.enrichment_llm_max_rpm,
            },
            indent=2,
        ),
        flush=True,
    )
    if args.dry_run or not job_ids:
        return

    outcome = await requeue(job_ids, dry_run=False)
    get_enrichment_worker().wake()
    print(json.dumps({"event": "requeued", **outcome}, indent=2), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
