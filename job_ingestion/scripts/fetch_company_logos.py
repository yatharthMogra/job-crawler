#!/usr/bin/env python3
"""Fetch and store normalized company logos for catalog companies."""

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
from app.ingestion.company_logos.worker import run_company_logo_batch


async def main(
    *,
    limit: int,
    pending_only: bool,
    board_token: str | None,
) -> None:
    async with AsyncSessionLocal() as db:
        result = await run_company_logo_batch(
            db,
            limit=limit,
            pending_only=pending_only,
            board_token=board_token,
        )
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch company logos into storage + companies table")
    parser.add_argument("--limit", type=int, default=100, help="Max companies to process")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process companies regardless of logo_status (default: pending/failed only)",
    )
    parser.add_argument("--board-token", type=str, default=None, help="Fetch logo for a single company")
    args = parser.parse_args()
    asyncio.run(
        main(
            limit=args.limit,
            pending_only=not args.all and args.board_token is None,
            board_token=args.board_token,
        )
    )
