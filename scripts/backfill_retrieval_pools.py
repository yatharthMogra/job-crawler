#!/usr/bin/env python3
"""Backfill retrieval_pools from stored normalized_roles (no LLM)."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

import os

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.ingestion.recommendation_fields import assign_retrieval_pools

BATCH_SIZE = 500


def _select_sql(board_token: str | None) -> str:
    company_filter = ""
    if board_token:
        company_filter = """
          AND EXISTS (
            SELECT 1 FROM companies c
            WHERE c.id = normalized_jobs.company_id
              AND c.board_token = :board_token
          )
        """
    return f"""
        SELECT id, normalized_roles, is_internship, is_new_grad
        FROM normalized_jobs
        WHERE is_active = TRUE
          AND processing_state = 'success'
          AND cardinality(retrieval_pools) = 0
          AND normalized_roles IS NOT NULL
          AND cardinality(normalized_roles) > 0
          {company_filter}
        ORDER BY id
        LIMIT :limit
    """


async def backfill(*, dry_run: bool, board_token: str | None) -> dict[str, int]:
    updated = 0
    skipped = 0
    select_sql = _select_sql(board_token)

    async with AsyncSessionLocal() as db:
        if dry_run:
            count_sql = select_sql.replace(
                "SELECT id, normalized_roles, is_internship, is_new_grad",
                "SELECT COUNT(*)",
            ).replace("ORDER BY id\n        LIMIT :limit", "")
            params: dict = {}
            if board_token:
                params["board_token"] = board_token
            updated = int((await db.execute(text(count_sql), params)).scalar() or 0)
            return {"updated": updated, "skipped_empty_pools": 0}

        while True:
            params = {"limit": BATCH_SIZE}
            if board_token:
                params["board_token"] = board_token

            rows = (await db.execute(text(select_sql), params)).all()
            if not rows:
                break

            for job_id, normalized_roles, is_internship, is_new_grad in rows:
                pools = assign_retrieval_pools(
                    list(normalized_roles or []),
                    bool(is_internship),
                    bool(is_new_grad),
                )
                if not pools:
                    skipped += 1
                    continue
                await db.execute(
                    text(
                        "UPDATE normalized_jobs SET retrieval_pools = :pools WHERE id = :id"
                    ),
                    {"pools": pools, "id": job_id},
                )
                updated += 1

            await db.commit()

    return {"updated": updated, "skipped_empty_pools": skipped}


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill retrieval_pools from normalized_roles (no LLM)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Count rows without updating")
    parser.add_argument(
        "--board-token",
        default=None,
        help="Scope to one company board_token (e.g. gevernova)",
    )
    args = parser.parse_args()

    result = await backfill(dry_run=args.dry_run, board_token=args.board_token)
    action = "would update" if args.dry_run else "updated"
    scope = f" for {args.board_token}" if args.board_token else ""
    print(f"{action} {result['updated']} jobs{scope}")
    if result["skipped_empty_pools"]:
        print(f"skipped {result['skipped_empty_pools']} rows (assign_retrieval_pools returned empty)")


if __name__ == "__main__":
    asyncio.run(main())
