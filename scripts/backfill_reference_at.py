#!/usr/bin/env python3
"""Backfill normalized_jobs.reference_at and recompute opportunity_score."""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

import os

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.ingestion.job_timestamp import resolve_reference_at
from app.ingestion.recommendation_fields import compute_opportunity_score

BATCH_SIZE = 500


async def backfill(*, dry_run: bool, force: bool) -> int:
    settings = get_settings()
    updated = 0
    where_clause = "TRUE" if force else "reference_at IS NULL"
    async with AsyncSessionLocal() as db:
        offset = 0
        while True:
            rows = (
                await db.execute(
                    text(
                        f"""
                        SELECT nj.id, nj.posted_at, rj.fetch_timestamp,
                               nj.salary_min, nj.salary_max, nj.application_effort
                        FROM normalized_jobs nj
                        JOIN raw_jobs rj ON nj.raw_job_id = rj.id
                        WHERE {where_clause}
                        ORDER BY nj.id
                        LIMIT :limit OFFSET :offset
                        """
                    ),
                    {"limit": BATCH_SIZE, "offset": offset},
                )
            ).all()
            if not rows:
                break

            for (
                job_id,
                posted_at,
                fetch_timestamp,
                salary_min,
                salary_max,
                application_effort,
            ) in rows:
                reference_at = resolve_reference_at(posted_at, fetch_timestamp)
                opportunity_score = compute_opportunity_score(
                    reference_at,
                    salary_min,
                    salary_max,
                    application_effort,
                    settings=settings,
                )
                if dry_run:
                    updated += 1
                    continue
                await db.execute(
                    text(
                        """
                        UPDATE normalized_jobs
                        SET reference_at = :reference_at,
                            opportunity_score = :opportunity_score,
                            opportunity_score_computed_at = :computed_at
                        WHERE id = :id
                        """
                    ),
                    {
                        "reference_at": reference_at,
                        "opportunity_score": opportunity_score,
                        "computed_at": datetime.now(timezone.utc),
                        "id": job_id,
                    },
                )
                updated += 1

            if not dry_run:
                await db.commit()
            offset += BATCH_SIZE

    return updated


async def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill reference_at on normalized_jobs")
    parser.add_argument("--dry-run", action="store_true", help="Count rows without updating")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recompute reference_at and opportunity_score for all jobs",
    )
    args = parser.parse_args()
    count = await backfill(dry_run=args.dry_run, force=args.force)
    action = "would update" if args.dry_run else "updated"
    print(f"{action} {count} jobs")


if __name__ == "__main__":
    asyncio.run(main())
