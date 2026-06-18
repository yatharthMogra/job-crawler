#!/usr/bin/env python3
"""Run full H-1B ingestion pipeline (load → normalize → aggregate → summary)."""

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
from app.ingestion.h1b.pipeline import run_h1b_ingestion


async def main(
    *,
    lca_path: Path | None,
    uscis_path: Path | None,
    uscis_fiscal_year: int | None,
    skip_load: bool,
) -> None:
    async with AsyncSessionLocal() as db:
        results = await run_h1b_ingestion(
            db,
            lca_path=lca_path,
            uscis_path=uscis_path,
            uscis_fiscal_year=uscis_fiscal_year,
            skip_load=skip_load,
        )
        print(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lca-file", type=Path, default=None)
    parser.add_argument("--uscis-file", type=Path, default=None)
    parser.add_argument("--uscis-fiscal-year", type=int, default=2024)
    parser.add_argument(
        "--skip-load",
        action="store_true",
        help="Re-run normalization/aggregation only (raw data already loaded)",
    )
    args = parser.parse_args()
    asyncio.run(
        main(
            lca_path=args.lca_file,
            uscis_path=args.uscis_file,
            uscis_fiscal_year=args.uscis_fiscal_year,
            skip_load=args.skip_load,
        )
    )
