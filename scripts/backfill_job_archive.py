#!/usr/bin/env python3
"""Backfill job_archive rows and job_archive_id for existing normalized_jobs.

Rollout sequence:
1. Deploy migration + pipeline + enrichment write-back
2. Run this script: python scripts/backfill_job_archive.py
3. Verify counts: python scripts/backfill_job_archive.py --count-only
4. Manually trigger cleanup: POST /maintenance/cleanup/active (watch batch logs)
5. Enable scheduler cron jobs after counts look correct
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))
os.chdir(JOB_INGESTION)

from sqlalchemy import func, select

from app.database import AsyncSessionLocal, engine
from app.ingestion.job_archive_sync import upsert_job_archive_from_normalized
from app.models.company import Company
from app.models.job_archive import JobArchive
from app.models.normalized_job import NormalizedJob


async def count_missing() -> dict:
    async with AsyncSessionLocal() as db:
        total = await db.scalar(select(func.count()).select_from(NormalizedJob)) or 0
        missing = await db.scalar(
            select(func.count())
            .select_from(NormalizedJob)
            .where(NormalizedJob.job_archive_id.is_(None))
        ) or 0
        archive_count = await db.scalar(select(func.count()).select_from(JobArchive)) or 0
        return {"normalized_jobs": total, "missing_archive_id": missing, "job_archive_rows": archive_count}


async def backfill(*, batch_size: int, dry_run: bool) -> dict:
    processed = 0
    updated = 0

    while True:
        async with AsyncSessionLocal() as db:
            rows = (
                await db.scalars(
                    select(NormalizedJob)
                    .where(NormalizedJob.job_archive_id.is_(None))
                    .limit(batch_size)
                )
            ).all()
            if not rows:
                break

            company_ids = {row.company_id for row in rows}
            companies = {
                company.id: company
                for company in (await db.scalars(select(Company).where(Company.id.in_(company_ids)))).all()
            }

            for normalized in rows:
                company = companies.get(normalized.company_id)
                if company is None:
                    continue
                if dry_run:
                    processed += 1
                    continue
                archive_id = await upsert_job_archive_from_normalized(db, normalized, company)
                normalized.job_archive_id = archive_id
                updated += 1
                processed += 1

            if not dry_run:
                await db.commit()

        if len(rows) < batch_size:
            break

    return {"processed": processed, "updated": updated, "dry_run": dry_run}


async def run_backfill(*, batch_size: int, dry_run: bool) -> None:
    try:
        before = await count_missing()
        print(json.dumps({"event": "backfill_start", **before}), flush=True)
        stats = await backfill(batch_size=batch_size, dry_run=dry_run)
        after = await count_missing()
        print(json.dumps({"event": "backfill_complete", **stats, "after": after}), flush=True)
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--count-only", action="store_true")
    args = parser.parse_args()

    if args.count_only:
        async def _count_only() -> None:
            try:
                print(json.dumps(await count_missing(), indent=2))
            finally:
                await engine.dispose()

        asyncio.run(_count_only())
        return

    asyncio.run(run_backfill(batch_size=args.batch_size, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
