#!/usr/bin/env python3
"""Build or refresh the job-term IDF corpus used for ATS BM25 scoring."""

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
from app.ingestion.idf_corpus import DEFAULT_BATCH_SIZE, build_idf_corpus


async def main(*, batch_size: int) -> None:
    async with AsyncSessionLocal() as db:
        result = await build_idf_corpus(db, batch_size=batch_size)
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build job-term IDF corpus for ATS scoring")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Jobs per DB fetch batch (default: {DEFAULT_BATCH_SIZE})",
    )
    args = parser.parse_args()
    asyncio.run(main(batch_size=args.batch_size))
