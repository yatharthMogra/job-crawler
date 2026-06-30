#!/usr/bin/env python3
"""Backfill job_identity_ledger from raw_jobs, then gap-fill from job_archive.

Rollout sequence:
1. Deploy migration
2. Run: python scripts/backfill_job_identity_ledger.py
3. Verify: python scripts/backfill_job_identity_ledger.py --count-only
4. Deploy pipeline code that reads/writes ledger
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

from sqlalchemy import text

from app.database import AsyncSessionLocal, engine

BACKFILL_PLACEHOLDER_HASH = "0" * 64


async def count_ledger() -> dict:
    async with AsyncSessionLocal() as db:
        ledger_count = await db.scalar(text("SELECT COUNT(*) FROM job_identity_ledger")) or 0
        raw_identities = await db.scalar(
            text(
                """
                SELECT COUNT(*) FROM (
                  SELECT DISTINCT company_id, external_job_id FROM raw_jobs
                ) t
                """
            )
        ) or 0
        archive_identities = await db.scalar(
            text(
                """
                SELECT COUNT(*) FROM (
                  SELECT DISTINCT company_id, external_job_id FROM job_archive
                ) t
                """
            )
        ) or 0
        return {
            "ledger_rows": ledger_count,
            "raw_identities": raw_identities,
            "archive_identities": archive_identities,
        }


async def backfill_from_raw_jobs(*, batch_size: int, dry_run: bool) -> int:
    inserted = 0
    while True:
        async with AsyncSessionLocal() as db:
            if dry_run:
                pending = await db.scalar(
                    text(
                        """
                        SELECT COUNT(*) FROM (
                          SELECT company_id, external_job_id
                          FROM raw_jobs
                          GROUP BY company_id, external_job_id
                        ) src
                        WHERE NOT EXISTS (
                          SELECT 1 FROM job_identity_ledger l
                          WHERE l.company_id = src.company_id
                            AND l.external_job_id = src.external_job_id
                        )
                        """
                    )
                ) or 0
                return pending

            result = await db.execute(
                text(
                    """
                    WITH src AS (
                      SELECT
                        company_id,
                        external_job_id,
                        (ARRAY_AGG(content_hash ORDER BY fetch_timestamp DESC))[1] AS content_hash,
                        MIN(fetch_timestamp) AS first_seen_at,
                        MAX(fetch_timestamp) AS last_seen_at
                      FROM raw_jobs
                      GROUP BY company_id, external_job_id
                    ),
                    batch AS (
                      SELECT src.*
                      FROM src
                      WHERE NOT EXISTS (
                        SELECT 1 FROM job_identity_ledger l
                        WHERE l.company_id = src.company_id
                          AND l.external_job_id = src.external_job_id
                      )
                      LIMIT :batch_size
                    )
                    INSERT INTO job_identity_ledger (
                      company_id, external_job_id, content_hash,
                      first_seen_at, last_seen_at, last_changed_at
                    )
                    SELECT
                      company_id, external_job_id, content_hash,
                      first_seen_at, last_seen_at, NULL
                    FROM batch
                    RETURNING company_id
                    """
                ),
                {"batch_size": batch_size},
            )
            rows = result.all()
            await db.commit()
            if not rows:
                break
            inserted += len(rows)
            if len(rows) < batch_size:
                break
    return inserted


async def backfill_gaps_from_archive(*, batch_size: int, dry_run: bool) -> int:
    inserted = 0
    while True:
        async with AsyncSessionLocal() as db:
            if dry_run:
                pending = await db.scalar(
                    text(
                        """
                        SELECT COUNT(*) FROM job_archive ja
                        WHERE NOT EXISTS (
                          SELECT 1 FROM job_identity_ledger l
                          WHERE l.company_id = ja.company_id
                            AND l.external_job_id = ja.external_job_id
                        )
                        """
                    )
                ) or 0
                return pending

            result = await db.execute(
                text(
                    """
                    WITH batch AS (
                      SELECT ja.company_id, ja.external_job_id, ja.created_at
                      FROM job_archive ja
                      WHERE NOT EXISTS (
                        SELECT 1 FROM job_identity_ledger l
                        WHERE l.company_id = ja.company_id
                          AND l.external_job_id = ja.external_job_id
                      )
                      LIMIT :batch_size
                    )
                    INSERT INTO job_identity_ledger (
                      company_id, external_job_id, content_hash,
                      first_seen_at, last_seen_at, last_changed_at
                    )
                    SELECT
                      company_id,
                      external_job_id,
                      :placeholder_hash,
                      created_at,
                      created_at,
                      NULL
                    FROM batch
                    RETURNING company_id
                    """
                ),
                {"batch_size": batch_size, "placeholder_hash": BACKFILL_PLACEHOLDER_HASH},
            )
            rows = result.all()
            await db.commit()
            if not rows:
                break
            inserted += len(rows)
            if len(rows) < batch_size:
                break
    return inserted


async def run_backfill(*, batch_size: int, dry_run: bool) -> None:
    try:
        before = await count_ledger()
        print(json.dumps({"event": "backfill_start", **before}), flush=True)
        from_raw = await backfill_from_raw_jobs(batch_size=batch_size, dry_run=dry_run)
        from_archive = await backfill_gaps_from_archive(batch_size=batch_size, dry_run=dry_run)
        after = await count_ledger()
        print(
            json.dumps(
                {
                    "event": "backfill_complete",
                    "from_raw_jobs": from_raw,
                    "from_job_archive_gaps": from_archive,
                    "dry_run": dry_run,
                    "after": after,
                }
            ),
            flush=True,
        )
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=5000)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--count-only", action="store_true")
    args = parser.parse_args()

    if args.count_only:

        async def _count_only() -> None:
            try:
                print(json.dumps(await count_ledger(), indent=2))
            finally:
                await engine.dispose()

        asyncio.run(_count_only())
        return

    asyncio.run(run_backfill(batch_size=args.batch_size, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
