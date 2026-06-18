#!/usr/bin/env python3
"""Normalize H-1B employer names and match to tracked companies."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import os

os.chdir(ROOT)

from app.database import AsyncSessionLocal
from app.ingestion.h1b.pipeline import normalize_all_employers


async def main(*, dry_run: bool) -> None:
    async with AsyncSessionLocal() as db:
        stats = await normalize_all_employers(db, dry_run=dry_run)
        print(stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(main(dry_run=args.dry_run))
