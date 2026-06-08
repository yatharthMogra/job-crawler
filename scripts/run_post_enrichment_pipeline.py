#!/usr/bin/env python3
"""Wipe stale companies, then run recommendation pipeline for remaining jobs."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "job_ingestion"))
sys.path.insert(0, str(ROOT / "recommendation_service"))

from sqlalchemy import text

from app.database import AsyncSessionLocal

WIPE_TOKENS = ["openai", "anthropic"]
E2E_TOKENS = [
    "slate", "basis", "achievers", "greenhouse", "linear",
    "ramp", "notion", "figma", "scaleai", "palantir",
]
CANDIDATE_ID = "6230dd88-b346-4e96-94fd-4a51c4500f34"
RECO_BASE = "http://localhost:8002"


async def wipe_companies(board_tokens: list[str]) -> None:
    tokens_sql = ", ".join(f"'{t}'" for t in board_tokens)
    async with AsyncSessionLocal() as db:
        before = await db.execute(
            text(
                f"""
                SELECT c.board_token, COUNT(nj.id) AS jobs
                FROM companies c
                LEFT JOIN normalized_jobs nj ON nj.company_id = c.id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY c.board_token ORDER BY c.board_token
                """
            )
        )
        print("WIPE BEFORE:", json.dumps([dict(r._mapping) for r in before], indent=2))

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
        deleted = await db.execute(
            text(
                f"""
                DELETE FROM raw_jobs
                WHERE company_id IN (
                    SELECT id FROM companies WHERE board_token IN ({tokens_sql})
                )
                """
            )
        )
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
        print(f"deleted_raw_jobs={deleted.rowcount}")

        after = await db.execute(
            text(
                f"""
                SELECT c.board_token, COUNT(nj.id) AS jobs
                FROM companies c
                LEFT JOIN normalized_jobs nj ON nj.company_id = c.id
                WHERE c.board_token IN ({tokens_sql})
                GROUP BY c.board_token ORDER BY c.board_token
                """
            )
        )
        print("WIPE AFTER:", json.dumps([dict(r._mapping) for r in after], indent=2))


async def e2e_job_stats() -> dict:
    tokens_sql = ", ".join(f"'{t}'" for t in E2E_TOKENS)
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    f"""
                    SELECT
                        COUNT(*) AS total,
                        COUNT(*) FILTER (WHERE nj.opportunity_score IS NOT NULL) AS enriched,
                        COUNT(*) FILTER (WHERE cardinality(nj.retrieval_pools) > 0) AS with_pools
                    FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token IN ({tokens_sql})
                      AND nj.processing_state = 'success'
                    """
                )
            )
        ).one()
        pools = await db.execute(
            text(
                f"""
                SELECT pool, COUNT(*) AS jobs
                FROM (
                    SELECT unnest(nj.retrieval_pools) AS pool
                    FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token IN ({tokens_sql})
                ) sub
                GROUP BY pool ORDER BY jobs DESC LIMIT 8
                """
            )
        )
        return {
            "jobs": dict(row._mapping),
            "top_pools": [dict(r._mapping) for r in pools],
        }


async def run_reco_pipeline(top_pools: list[str]) -> dict:
    report: dict = {}
    async with httpx.AsyncClient(timeout=120.0) as client:
        sub = await client.post(
            f"{RECO_BASE}/subscriptions",
            json={"candidate_id": CANDIDATE_ID, "pool_names": top_pools},
        )
        sub.raise_for_status()
        report["subscriptions"] = sub.json()

        dash = await client.get(
            f"{RECO_BASE}/dashboard/jobs",
            params={"candidate_id": CANDIDATE_ID, "limit": 10},
        )
        dash.raise_for_status()
        report["dashboard"] = {
            "total": dash.json().get("total"),
            "returned": len(dash.json().get("jobs", [])),
            "top_titles": [j.get("title") for j in dash.json().get("jobs", [])[:5]],
        }

        notif = await client.post(f"{RECO_BASE}/notifications/run")
        notif.raise_for_status()
        report["notifications_trigger"] = notif.json()

        await asyncio.sleep(3)

    # Read latest batch from DB (reco session)
    for key in list(sys.modules):
        if key == "app" or key.startswith("app."):
            del sys.modules[key]
    sys.path.insert(0, str(ROOT / "recommendation_service"))
    from app.database import AsyncSessionLocal as RecoSession

    async with RecoSession() as db:
        batch = (
            await db.execute(
                text(
                    """
                    SELECT status, jobs_in_pools, jobs_after_filter, jobs_sent,
                           skip_reason, email_delivered
                    FROM notification_batches
                    WHERE candidate_id = :cid
                    ORDER BY created_at DESC LIMIT 1
                    """
                ),
                {"cid": CANDIDATE_ID},
            )
        ).mappings().first()
        report["latest_batch"] = dict(batch) if batch else None

    return report


async def main() -> None:
    await wipe_companies(WIPE_TOKENS)
    stats = await e2e_job_stats()
    print("E2E JOB STATS:", json.dumps(stats, indent=2, default=str))

    top_pools = [p["pool"] for p in stats["top_pools"][:5]]
    if not top_pools:
        print("No pools found — aborting reco pipeline")
        return

    reco = await run_reco_pipeline(top_pools)
    print("RECO PIPELINE:", json.dumps(reco, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
