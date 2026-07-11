#!/usr/bin/env python3
"""Backfill content embeddings for normalized jobs missing embeddings."""

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

from app.database import AsyncSessionLocal
from app.ingestion.ats_enrichment import DEFAULT_BACKFILL_BATCH_SIZE, backfill_missing_job_embeddings


async def main(*, batch_size: int, max_batches: int | None) -> None:
    async with AsyncSessionLocal() as db:
        result = await backfill_missing_job_embeddings(
            db,
            batch_size=batch_size,
            max_batches=max_batches,
        )
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Backfill job embeddings and pool percentile cutoffs for rows with NULL content_embedding",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BACKFILL_BATCH_SIZE,
        help=f"Jobs per batch (default: {DEFAULT_BACKFILL_BATCH_SIZE})",
    )
    parser.add_argument(
        "--max-batches",
        type=int,
        default=None,
        help="Stop after N batches (default: run until no NULL embeddings remain)",
    )
    args = parser.parse_args()
    asyncio.run(main(batch_size=args.batch_size, max_batches=args.max_batches))
