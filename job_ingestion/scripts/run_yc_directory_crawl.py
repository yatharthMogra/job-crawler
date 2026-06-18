#!/usr/bin/env python3
"""Run YC company directory crawl (Phase 1)."""

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

from app.schedulers.yc_ingestion import run_yc_directory_crawl_job


async def main(*, dry_run: bool) -> None:
    summary = await run_yc_directory_crawl_job(dry_run=dry_run)
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl YC company directory for ATS discovery")
    parser.add_argument("--dry-run", action="store_true", help="Discover only; do not upsert companies")
    args = parser.parse_args()
    asyncio.run(main(dry_run=args.dry_run))
