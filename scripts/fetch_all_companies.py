#!/usr/bin/env python3
"""Seed companies and fetch jobs for a subset. Enrichment is handled by job_ingestion."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import socket
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))
os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.config import Settings
from app.database import AsyncSessionLocal
from app.utils.seed import seed_companies

API_BASE = "http://localhost:8000"
REPORT_PATH = ROOT / "exports" / "fetch_all_companies_report.json"
COMPANIES_JSON = JOB_INGESTION / "data" / "companies.json"


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


async def _stats() -> dict:
    async with AsyncSessionLocal() as db:
        companies = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) AS active_companies,
                      COUNT(*) FILTER (
                        WHERE EXISTS (
                          SELECT 1 FROM normalized_jobs nj
                          WHERE nj.company_id = companies.id AND nj.is_active
                        )
                      ) AS companies_with_jobs
                    FROM companies
                    WHERE is_active
                    """
                )
            )
        ).one()
        jobs = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(*) AS total_jobs,
                      COUNT(*) FILTER (WHERE processing_state = 'success') AS success,
                      COUNT(*) FILTER (WHERE opportunity_score IS NOT NULL) AS enriched,
                      COUNT(*) FILTER (WHERE processing_state = 'failed') AS failed
                    FROM normalized_jobs
                    WHERE is_active
                    """
                )
            )
        ).one()
        queue = (
            await db.execute(
                text(
                    """
                    SELECT status, COUNT(*) AS jobs
                    FROM enrichment_queue
                    GROUP BY status
                    """
                )
            )
        ).all()
        fresh = (
            await db.execute(
                text(
                    """
                    SELECT COUNT(*) AS fresh_jobs
                    FROM normalized_jobs
                    WHERE is_active
                      AND processing_state = 'success'
                      AND posted_at >= NOW() - make_interval(days => :job_max_age_days)
                    """
                ),
                {"job_max_age_days": Settings().job_max_age_days},
            )
        ).one()
        return {
            **dict(companies._mapping),
            **dict(jobs._mapping),
            **dict(fresh._mapping),
            "queue": {row.status: row.jobs for row in queue},
        }


async def select_board_tokens(*, limit: int) -> list[str]:
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    """
                    SELECT c.board_token, COUNT(nj.id) AS jobs
                    FROM companies c
                    LEFT JOIN normalized_jobs nj
                      ON nj.company_id = c.id AND nj.is_active
                    WHERE c.is_active
                    GROUP BY c.board_token
                    ORDER BY jobs ASC, c.board_token ASC
                    LIMIT :limit
                    """
                ),
                {"limit": limit},
            )
        ).all()
        return [row.board_token for row in rows]


async def set_fetch_scope(board_tokens: set[str]) -> None:
    payload = json.loads(COMPANIES_JSON.read_text(encoding="utf-8"))
    json_active = {
        item["board_token"]
        for item in payload
        if item.get("board_token") and item.get("is_active", True)
    }
    allowed = board_tokens & json_active
    async with AsyncSessionLocal() as db:
        await db.execute(
            text(
                """
                UPDATE companies
                SET is_active = board_token = ANY(:tokens)
                """
            ),
            {"tokens": list(allowed)},
        )
        await db.commit()


async def restore_companies_from_json() -> dict:
    async with AsyncSessionLocal() as db:
        return await seed_companies(db)


async def company_queue_pending(board_token: str) -> int:
    async with AsyncSessionLocal() as db:
        return int(
            await db.scalar(
                text(
                    """
                    SELECT COUNT(*)
                    FROM enrichment_queue eq
                    JOIN normalized_jobs nj ON nj.id = eq.normalized_job_id
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token = :token
                      AND eq.status IN ('queued', 'cooldown', 'in_progress')
                    """
                ),
                {"token": board_token},
            )
            or 0
        )


async def company_enrichment_status(board_token: str) -> dict:
    async with AsyncSessionLocal() as db:
        row = (
            await db.execute(
                text(
                    """
                    SELECT
                      COUNT(nj.id) AS total_jobs,
                      COUNT(*) FILTER (WHERE nj.processing_state = 'success') AS enriched,
                      COUNT(*) FILTER (WHERE nj.processing_state = 'pending') AS pending
                    FROM normalized_jobs nj
                    JOIN companies c ON c.id = nj.company_id
                    WHERE c.board_token = :token AND nj.is_active
                    """
                ),
                {"token": board_token},
            )
        ).one()
        queue = (
            await db.execute(
                text(
                    """
                    SELECT eq.status, COUNT(*) AS jobs
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
        return {**dict(row._mapping), "queue": {r.status: r.jobs for r in queue}}


async def trigger_pipeline(settings: Settings) -> dict:
    if _port_open("127.0.0.1", 8000):
        async with httpx.AsyncClient(timeout=600.0) as client:
            trigger = await client.post(f"{API_BASE}/pipeline/trigger")
            trigger.raise_for_status()
            return trigger.json()

    from app.ingestion.pipeline import run_pipeline

    async with AsyncSessionLocal() as db:
        snapshot = await run_pipeline(db=db, run_type="manual", settings=settings)
    return snapshot.__dict__


async def process_company_sequential(
    board_token: str,
    settings: Settings,
    *,
    ashby_cooldown_s: float,
) -> dict:
    payload = json.loads(COMPANIES_JSON.read_text(encoding="utf-8"))
    by_token = {item["board_token"]: item for item in payload if item.get("board_token")}
    meta = by_token.get(board_token, {})

    print(json.dumps({"event": "company_start", "board_token": board_token, "platform": meta.get("platform")}), flush=True)

    await restore_companies_from_json()
    await set_fetch_scope({board_token})

    pipeline = await trigger_pipeline(settings)
    print(json.dumps({"event": "pipeline", "board_token": board_token, **pipeline}, default=str), flush=True)

    await restore_companies_from_json()

    company_after_fetch = await company_enrichment_status(board_token)
    print(json.dumps({"event": "after_fetch", "board_token": board_token, **company_after_fetch}, default=str), flush=True)

    if pipeline.get("status") == "failed" or pipeline.get("jobs_new", 0) == 0:
        if company_after_fetch.get("total_jobs", 0) == 0:
            return {
                "board_token": board_token,
                "pipeline": pipeline,
                "enrichment": company_after_fetch,
                "status": "fetch_failed",
            }

    result = {
        "board_token": board_token,
        "pipeline": pipeline,
        "enrichment": company_after_fetch,
        "status": "queued_for_enrichment",
    }
    print(json.dumps({"event": "company_done", **result}, default=str), flush=True)

    if meta.get("platform") == "ashby" and ashby_cooldown_s > 0:
        print(json.dumps({"event": "ashby_cooldown", "seconds": ashby_cooldown_s}), flush=True)
        await asyncio.sleep(ashby_cooldown_s)

    return result


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=29, help="Number of companies to fetch (default: half of 58)")
    parser.add_argument("--half", action="store_true", help="Fetch half of active companies in companies.json")
    parser.add_argument(
        "--tokens",
        nargs="+",
        help="Fetch specific board tokens sequentially (enrichment handled by job_ingestion)",
    )
    parser.add_argument("--ashby-cooldown-s", type=float, default=45.0)
    parser.add_argument("--dry-run", action="store_true", help="Show selected companies and stats only")
    args = parser.parse_args()

    payload = json.loads(COMPANIES_JSON.read_text(encoding="utf-8"))
    active_count = sum(1 for item in payload if item.get("is_active", True))
    limit = max(1, active_count // 2) if args.half else args.limit

    settings = Settings()
    if args.tokens:
        selected = args.tokens
    else:
        selected = await select_board_tokens(limit=limit)

    print(
        json.dumps(
            {
                "active_in_json": active_count,
                "fetch_limit": limit,
                "selected_companies": selected,
                "gemini_model": settings.gemini_model,
                "extraction_version": settings.extraction_version,
            },
            indent=2,
        ),
        flush=True,
    )

    before = await _stats()
    print(json.dumps({"event": "before", **before}, default=str), flush=True)

    if args.dry_run:
        return

    report: dict = {
        "selected_companies": selected,
        "before": before,
    }

    if args.tokens:
        company_results: list[dict] = []
        for token in selected:
            company_results.append(
                await process_company_sequential(
                    token,
                    settings,
                    ashby_cooldown_s=args.ashby_cooldown_s,
                )
            )
        report["companies"] = company_results
        report["after"] = await _stats()
        REPORT_PATH.parent.mkdir(exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
        print(json.dumps({"event": "final", **report["after"]}, default=str), flush=True)
        print(f"wrote {REPORT_PATH}", flush=True)
        if any(r.get("status") == "fetch_failed" for r in company_results):
            failed = [r for r in company_results if r.get("status") != "queued_for_enrichment"]
            print(json.dumps({"event": "partial_failure", "failed": failed}, default=str), flush=True)
            raise SystemExit(1)
        return

    seed_result = await restore_companies_from_json()
    print(json.dumps({"event": "seed", **seed_result}), flush=True)

    await set_fetch_scope(set(selected))
    async with AsyncSessionLocal() as db:
        active_for_fetch = await db.scalar(text("SELECT COUNT(*) FROM companies WHERE is_active"))

    print(json.dumps({"event": "fetch_scope", "active_companies": active_for_fetch}), flush=True)

    pipeline = await trigger_pipeline(settings)
    print(json.dumps({"event": "pipeline", **pipeline}, default=str), flush=True)
    report["pipeline"] = pipeline

    restored = await restore_companies_from_json()
    print(json.dumps({"event": "restore_active_flags", **restored}), flush=True)

    report["after"] = await _stats()
    print(json.dumps({"event": "final", **report["after"]}, default=str), flush=True)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(f"wrote {REPORT_PATH}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
