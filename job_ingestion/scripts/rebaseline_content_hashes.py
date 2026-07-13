#!/usr/bin/env python3
"""Recompute canonical content hashes on latest raw_jobs and job_identity_ledger rows."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.ingestion.job_content_hash import compute_job_content_hash
from app.ingestion.job_identity_ledger import upsert_ledger_entry
from app.models.company import Company
from app.models.raw_job import RawJob


async def _latest_raw_jobs_for_company(db, company_id: UUID) -> list[RawJob]:
    stmt = (
        select(RawJob)
        .where(RawJob.company_id == company_id)
        .order_by(RawJob.external_job_id.asc(), RawJob.fetch_timestamp.desc())
    )
    rows = (await db.scalars(stmt)).all()
    latest: dict[str, RawJob] = {}
    for row in rows:
        latest.setdefault(row.external_job_id, row)
    return list(latest.values())


async def main(
    *,
    batch_size: int,
    dry_run: bool,
    company_id: UUID | None,
    board_token: str | None,
    active_only: bool,
) -> None:
    raw_jobs_updated = 0
    ledger_upserted = 0
    companies_processed = 0

    async with AsyncSessionLocal() as db:
        stmt = select(Company).order_by(Company.name.asc())
        if company_id is not None:
            stmt = stmt.where(Company.id == company_id)
        if board_token is not None:
            stmt = stmt.where(Company.board_token == board_token)
        if active_only:
            stmt = stmt.where(Company.is_active.is_(True))
        companies = (await db.scalars(stmt)).all()

        for company in companies:
            latest_rows = await _latest_raw_jobs_for_company(db, company.id)
            if not latest_rows:
                continue
            companies_processed += 1
            for row in latest_rows:
                if not isinstance(row.raw_api_response, dict):
                    continue
                new_hash = compute_job_content_hash(row.raw_api_response, company.platform)
                if row.content_hash != new_hash:
                    raw_jobs_updated += 1
                    if not dry_run:
                        row.content_hash = new_hash
                ledger_upserted += 1
                if not dry_run:
                    await upsert_ledger_entry(
                        db,
                        company.id,
                        row.external_job_id,
                        new_hash,
                        seen_at=row.fetch_timestamp,
                    )
            if not dry_run and companies_processed % batch_size == 0:
                await db.commit()

        if not dry_run:
            await db.commit()

    print(
        {
            "dry_run": dry_run,
            "companies_processed": companies_processed,
            "raw_jobs_updated": raw_jobs_updated,
            "ledger_upserted": ledger_upserted,
        }
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebaseline canonical content hashes from raw_jobs")
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--company-id", type=str, default=None)
    parser.add_argument("--board-token", type=str, default=None)
    parser.add_argument("--all", action="store_true", help="Include inactive companies")
    args = parser.parse_args()
    company_uuid = UUID(args.company_id) if args.company_id else None
    asyncio.run(
        main(
            batch_size=args.batch_size,
            dry_run=args.dry_run,
            company_id=company_uuid,
            board_token=args.board_token,
            active_only=not args.all,
        )
    )
