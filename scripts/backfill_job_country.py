#!/usr/bin/env python3
"""Backfill normalized_jobs.job_country from location strings."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

import os

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.ingestion.extractor.deterministic import extract_job_country

BATCH_SIZE = 500


async def backfill(*, dry_run: bool, force: bool) -> int:
    updated = 0
    where_clause = "is_active" if force else "is_active AND job_country IS NULL"
    async with AsyncSessionLocal() as db:
        offset = 0
        while True:
            rows = (
                await db.execute(
                    text(
                        f"""
                        SELECT id, location
                        FROM normalized_jobs
                        WHERE {where_clause}
                        ORDER BY id
                        LIMIT :limit OFFSET :offset
                        """
                    ),
                    {"limit": BATCH_SIZE, "offset": offset},
                )
            ).all()
            if not rows:
                break

            for job_id, location in rows:
                country = extract_job_country(location)
                if dry_run:
                    updated += 1
                    continue
                await db.execute(
                    text("UPDATE normalized_jobs SET job_country = :country WHERE id = :id"),
                    {"country": country, "id": job_id},
                )
                updated += 1

            if not dry_run:
                await db.commit()
            offset += BATCH_SIZE

    return updated


async def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill job_country on active jobs")
    parser.add_argument("--dry-run", action="store_true", help="Count rows without updating")
    parser.add_argument("--force", action="store_true", help="Recompute job_country for all active jobs")
    args = parser.parse_args()
    count = await backfill(dry_run=args.dry_run, force=args.force)
    action = "would update" if args.dry_run else "updated"
    print(f"{action} {count} jobs")


if __name__ == "__main__":
    asyncio.run(main())
