#!/usr/bin/env python3
"""Wipe, fetch, and enrich one company at a time to avoid Gemini rate limits."""

from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "job_ingestion"))

from sqlalchemy import text

from app.database import AsyncSessionLocal

COMPANIES_JSON = ROOT / "job_ingestion" / "data" / "companies.json"
API_BASE = "http://localhost:8000"

# Smallest first — easier to validate early batches.
BATCH_2_TOKENS = ["ramp", "notion", "figma", "scaleai", "palantir"]

# Keep first E2E batch inactive during fetch so we do not re-crawl them.
BATCH_1_TOKENS = ["slate", "basis", "achievers", "greenhouse", "linear"]


def set_active_company(active_token: str) -> None:
    payload = json.loads(COMPANIES_JSON.read_text(encoding="utf-8"))
    for item in payload:
        token = item["board_token"]
        if token == active_token:
            item["is_active"] = True
        elif token in BATCH_2_TOKENS or token in BATCH_1_TOKENS:
            item["is_active"] = False
    COMPANIES_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def restore_all_e2e_active() -> None:
    payload = json.loads(COMPANIES_JSON.read_text(encoding="utf-8"))
    e2e = set(BATCH_1_TOKENS + BATCH_2_TOKENS)
    for item in payload:
        if item["board_token"] in e2e:
            item["is_active"] = True
    COMPANIES_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


async def wipe_company(board_token: str) -> int:
    async with AsyncSessionLocal() as db:
        before = await db.scalar(
            text(
                """
                SELECT COUNT(*) FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                WHERE c.board_token = :token
                """
            ),
            {"token": board_token},
        )
        await db.execute(
            text(
                """
                DELETE FROM notification_job_history
                WHERE job_id IN (
                    SELECT nj.id FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token = :token
                )
                """
            ),
            {"token": board_token},
        )
        result = await db.execute(
            text(
                """
                DELETE FROM raw_jobs
                WHERE company_id IN (
                    SELECT id FROM companies WHERE board_token = :token
                )
                """
            ),
            {"token": board_token},
        )
        await db.execute(
            text(
                """
                DELETE FROM company_run_results
                WHERE company_id IN (
                    SELECT id FROM companies WHERE board_token = :token
                )
                """
            ),
            {"token": board_token},
        )
        await db.commit()
        print(f"  wiped {board_token}: {before} normalized jobs, {result.rowcount} raw_jobs deleted")
        return int(before or 0)


async def enrichment_status(board_token: str) -> dict:
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                        COUNT(*) AS total,
                        COUNT(*) FILTER (WHERE nj.processing_state = 'success') AS success,
                        COUNT(*) FILTER (WHERE nj.opportunity_score IS NOT NULL) AS enriched,
                        COUNT(*) FILTER (WHERE nj.processing_state = 'failed') AS failed
                    FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token = :token
                    """
                ),
                {"token": board_token},
            )
        ).one()
        queue = (
            await db.execute(
                text(
                    """
                    SELECT eq.status, COUNT(*)
                    FROM enrichment_queue eq
                    JOIN normalized_jobs nj ON nj.id = eq.normalized_job_id
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token = :token
                    GROUP BY eq.status
                    """
                ),
                {"token": board_token},
            )
        ).all()
        return {
            "total": row.total,
            "success": row.success,
            "enriched": row.enriched,
            "failed": row.failed,
            "queue": dict(queue),
        }


async def wait_for_enrichment(board_token: str, timeout_s: int = 7200) -> dict:
    start = time.monotonic()
    last_line = ""
    while time.monotonic() - start < timeout_s:
        status = await enrichment_status(board_token)
        line = (
            f"  enrich {board_token}: total={status['total']} enriched={status['enriched']} "
            f"failed={status['failed']} queue={status['queue']}"
        )
        if line != last_line:
            print(line)
            last_line = line

        total = status["total"]
        if total == 0:
            await asyncio.sleep(5)
            continue
        if status["enriched"] >= total and status["failed"] == 0:
            return status
        if status["failed"] > 0 and status["queue"].get("queued", 0) == 0 and status["queue"].get("in_progress", 0) == 0:
            print(f"  WARNING: {status['failed']} failed jobs with empty queue for {board_token}")
            return status
        await asyncio.sleep(15)
    raise TimeoutError(f"Enrichment timed out for {board_token}")


async def process_company(client: httpx.AsyncClient, board_token: str) -> dict:
    print(f"\n=== {board_token.upper()} ===")
    set_active_company(board_token)
    await wipe_company(board_token)

    seed = await client.post(f"{API_BASE}/companies/seed")
    seed.raise_for_status()
    print(f"  seed: {seed.json()}")

    trigger = await client.post(f"{API_BASE}/pipeline/trigger")
    trigger.raise_for_status()
    run = trigger.json()
    print(f"  pipeline: run_id={run.get('id')} jobs_new={run.get('jobs_new')} status={run.get('status')}")

    final = await wait_for_enrichment(board_token)
    print(f"  done {board_token}: {final}")
    return {"board_token": board_token, "pipeline_run": run, "enrichment": final}


async def main() -> None:
    tokens = BATCH_2_TOKENS
    if len(sys.argv) > 1:
        tokens = sys.argv[1:]

    results: list[dict] = []
    async with httpx.AsyncClient(timeout=600.0) as client:
        for token in tokens:
            results.append(await process_company(client, token))

        restore_all_e2e_active()
        seed = await client.post(f"{API_BASE}/companies/seed")
        seed.raise_for_status()
        print(f"\nrestored all E2E active: {seed.json()}")

    print("\nSUMMARY:")
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
