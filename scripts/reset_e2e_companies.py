#!/usr/bin/env python3
"""Wipe job ingestion + notification history for selected company board_tokens."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "job_ingestion"))

from sqlalchemy import text

from app.database import AsyncSessionLocal

TARGET_TOKENS = ["slate", "basis", "achievers", "greenhouse", "linear"]


async def main() -> None:
    tokens_sql = ", ".join(f"'{t}'" for t in TARGET_TOKENS)
    async with AsyncSessionLocal() as db:
        before = await db.execute(
            text(
                f"""
                SELECT c.board_token, COUNT(nj.id) AS jobs
                FROM companies c
                LEFT JOIN normalized_jobs nj ON nj.company_id = c.id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY c.board_token
                ORDER BY c.board_token
                """
            )
        )
        print("BEFORE:", json.dumps([dict(r._mapping) for r in before], indent=2))

        await db.execute(
            text(
                f"""
                DELETE FROM notification_job_history
                WHERE job_id IN (
                    SELECT nj.id FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token IN ({tokens_sql})
                )
                """
            )
        )
        result = await db.execute(
            text(
                f"""
                DELETE FROM raw_jobs
                WHERE company_id IN (
                    SELECT id FROM companies WHERE board_token IN ({tokens_sql})
                )
                """
            )
        )
        deleted_raw = result.rowcount
        await db.execute(
            text(
                f"""
                DELETE FROM company_run_results
                WHERE company_id IN (
                    SELECT id FROM companies WHERE board_token IN ({tokens_sql})
                )
                """
            )
        )
        await db.commit()

        after = await db.execute(
            text(
                f"""
                SELECT c.board_token, COUNT(nj.id) AS jobs
                FROM companies c
                LEFT JOIN normalized_jobs nj ON nj.company_id = c.id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY c.board_token
                ORDER BY c.board_token
                """
            )
        )
        print("AFTER:", json.dumps([dict(r._mapping) for r in after], indent=2))
        print(f"deleted_raw_jobs={deleted_raw}")


if __name__ == "__main__":
    asyncio.run(main())
