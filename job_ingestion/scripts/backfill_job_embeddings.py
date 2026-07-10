#!/usr/bin/env python3
"""Backfill content embeddings for normalized jobs."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.ingestion.ats_enrichment import apply_job_ats_enrichment
from app.models.normalized_job import NormalizedJob


async def main(*, limit: int) -> None:
    updated = 0
    async with AsyncSessionLocal() as db:
        jobs = (
            await db.scalars(
                select(NormalizedJob)
                .where(
                    NormalizedJob.is_active.is_(True),
                    NormalizedJob.processing_state == "success",
                )
                .order_by(NormalizedJob.updated_at.desc())
                .limit(limit)
            )
        ).all()
        for job in jobs:
            await apply_job_ats_enrichment(db, job)
            updated += 1
        await db.commit()
    print(json.dumps({"updated": updated}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill job embeddings and pool percentile cutoffs")
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()
    asyncio.run(main(limit=args.limit))
