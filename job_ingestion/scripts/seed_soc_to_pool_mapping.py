#!/usr/bin/env python3
"""Seed soc_to_pool_mapping from h1b_integration_guide.md."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import os

os.chdir(ROOT)

from sqlalchemy.dialects.postgresql import insert

from app.database import AsyncSessionLocal
from app.ingestion.h1b.soc_seed_data import SOC_TO_POOL_SEED
from app.models.h1b import SocToPoolMapping


async def seed(*, dry_run: bool) -> int:
    async with AsyncSessionLocal() as db:
        if dry_run:
            print(f"Would upsert {len(SOC_TO_POOL_SEED)} SOC mappings")
            return len(SOC_TO_POOL_SEED)

        for row in SOC_TO_POOL_SEED:
            stmt = (
                insert(SocToPoolMapping)
                .values(**row)
                .on_conflict_do_nothing(index_elements=["soc_code"])
            )
            await db.execute(stmt)
        await db.commit()
        print(f"Seeded {len(SOC_TO_POOL_SEED)} SOC mappings (append-only)")
        return len(SOC_TO_POOL_SEED)


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed soc_to_pool_mapping table")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(seed(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
