#!/usr/bin/env python3
"""Backfill dedup_fingerprint on existing normalized_jobs rows."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.ingestion.dedup import build_dedup_fingerprint
from app.models.normalized_job import NormalizedJob


async def main(*, batch_size: int, active_only: bool) -> None:
    updated = 0
    async with AsyncSessionLocal() as db:
        offset = 0
        while True:
            stmt = select(NormalizedJob).order_by(NormalizedJob.id).offset(offset).limit(batch_size)
            if active_only:
                stmt = stmt.where(NormalizedJob.is_active.is_(True))
            rows = (await db.scalars(stmt)).all()
            if not rows:
                break
            for row in rows:
                row.dedup_fingerprint = build_dedup_fingerprint(
                    row.company_name,
                    row.title,
                    row.location,
                )
                updated += 1
            await db.commit()
            offset += batch_size
    print({"updated": updated})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill dedup_fingerprint values")
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--all", action="store_true", help="Include inactive jobs")
    args = parser.parse_args()
    asyncio.run(main(batch_size=args.batch_size, active_only=not args.all))
