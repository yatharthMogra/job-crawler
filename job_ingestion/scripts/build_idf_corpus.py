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
from app.ingestion.idf_corpus import build_idf_corpus


async def main() -> None:
    async with AsyncSessionLocal() as db:
        result = await build_idf_corpus(db)
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build job-term IDF corpus for ATS scoring")
    _ = parser.parse_args()
    asyncio.run(main())
