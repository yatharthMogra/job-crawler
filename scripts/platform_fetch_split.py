#!/usr/bin/env python3
"""Live-fetch all seed companies and report job counts split by ATS platform."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

from app.ingestion.fetcher import fetch_company_jobs  # noqa: E402
from app.models.company import Company  # noqa: E402

COMPANIES_JSON = JOB_INGESTION / "data" / "companies.json"
DEFAULT_OUT = ROOT / "exports" / "platform_fetch_split.json"


def _make_company(row: dict) -> Company:
    return Company(
        id=uuid4(),
        name=row["company"],
        platform=row["platform"],
        board_token=row["board_token"],
        platform_config=row.get("platform_config"),
        is_active=True,
    )


async def _fetch_one(company: Company, sem: asyncio.Semaphore, timeout_s: int) -> dict:
    async with sem:
        started = time.perf_counter()
        task = asyncio.create_task(fetch_company_jobs(company))
        try:
            jobs = await asyncio.wait_for(asyncio.shield(task), timeout=timeout_s)
            return {
                "name": company.name,
                "platform": company.platform,
                "board_token": company.board_token,
                "status": "ok",
                "jobs": len(jobs),
                "seconds": round(time.perf_counter() - started, 2),
            }
        except (asyncio.TimeoutError, TimeoutError):
            task.cancel()
            return {
                "name": company.name,
                "platform": company.platform,
                "board_token": company.board_token,
                "status": "timeout",
                "jobs": 0,
                "error": f"exceeded {timeout_s}s",
                "seconds": timeout_s,
            }
        except Exception as exc:  # noqa: BLE001
            return {
                "name": company.name,
                "platform": company.platform,
                "board_token": company.board_token,
                "status": "error",
                "jobs": 0,
                "error": str(exc)[:300],
                "seconds": round(time.perf_counter() - started, 2),
            }


def _aggregate(results: list[dict], *, elapsed: float, timeout_s: int) -> dict:
    by_platform: dict[str, dict] = defaultdict(
        lambda: {
            "companies": 0,
            "companies_ok": 0,
            "companies_failed": 0,
            "companies_timeout": 0,
            "jobs_fetched": 0,
        }
    )
    for row in results:
        stats = by_platform[row["platform"]]
        stats["companies"] += 1
        if row["status"] == "ok":
            stats["companies_ok"] += 1
            stats["jobs_fetched"] += row["jobs"]
        elif row["status"] == "timeout":
            stats["companies_timeout"] += 1
            stats["companies_failed"] += 1
        else:
            stats["companies_failed"] += 1

    total_jobs = sum(row["jobs"] for row in results)
    total_ok = sum(1 for row in results if row["status"] == "ok")
    return {
        "elapsed_seconds": elapsed,
        "company_timeout_seconds": timeout_s,
        "total_companies": len(results),
        "successful_companies": total_ok,
        "failed_companies": len(results) - total_ok,
        "total_jobs_fetched": total_jobs,
        "by_platform": dict(sorted(by_platform.items(), key=lambda kv: -kv[1]["jobs_fetched"])),
        "companies": sorted(results, key=lambda r: (-r["jobs"], r["platform"], r["name"])),
        "failures": [row for row in results if row["status"] != "ok"],
    }


def _print_summary(summary: dict) -> None:
    total_jobs = summary["total_jobs_fetched"]
    total = summary["total_companies"]
    ok = summary["successful_companies"]
    elapsed = summary["elapsed_seconds"]
    print("=" * 80)
    print(f"SOURCE SPLIT — {total_jobs:,} jobs from {ok}/{total} companies ({elapsed}s)")
    print("=" * 80)
    print(f"{'Platform':<14} {'Cos':>5} {'OK':>4} {'Fail':>5} {'T/O':>4} {'Jobs':>10} {'%':>7}")
    print("-" * 80)
    for platform, stats in summary["by_platform"].items():
        pct = (stats["jobs_fetched"] / total_jobs * 100) if total_jobs else 0
        print(
            f"{platform:<14} {stats['companies']:>5} {stats['companies_ok']:>4} "
            f"{stats['companies_failed']:>5} {stats['companies_timeout']:>4} "
            f"{stats['jobs_fetched']:>10,} {pct:>6.1f}%"
        )
    print("-" * 80)
    timeouts = sum(1 for row in summary["companies"] if row["status"] == "timeout")
    print(
        f"{'TOTAL':<14} {total:>5} {ok:>4} {total - ok:>5} {timeouts:>4} "
        f"{total_jobs:>10,} {'100.0%':>7}"
    )


async def _run(
    *,
    platforms: set[str] | None,
    concurrency: int,
    timeout_s: int,
    out_path: Path,
) -> dict:
    rows = json.loads(COMPANIES_JSON.read_text(encoding="utf-8"))
    active = [row for row in rows if row.get("is_active", True)]
    if platforms:
        active = [row for row in active if row["platform"] in platforms]

    sem = asyncio.Semaphore(concurrency)
    companies = [_make_company(row) for row in active]
    started = time.time()
    done = 0
    results: list[dict] = []

    async def run_one(company: Company) -> dict:
        nonlocal done
        row = await _fetch_one(company, sem, timeout_s)
        done += 1
        if done % 10 == 0 or done == len(companies):
            print(f"progress {done}/{len(companies)}", flush=True)
        return row

    results = await asyncio.gather(*(run_one(company) for company in companies))
    summary = _aggregate(results, elapsed=round(time.time() - started, 1), timeout_s=timeout_s)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    _print_summary(summary)
    print(f"\nReport: {out_path.resolve()}")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--timeout-s", type=int, default=120)
    parser.add_argument("--workday-timeout-s", type=int, default=300)
    parser.add_argument(
        "--platform",
        action="append",
        help="Only fetch this platform (repeatable). Default: all platforms.",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    platforms = set(args.platform) if args.platform else None
    if platforms:
        asyncio.run(
            _run(
                platforms=platforms,
                concurrency=args.concurrency,
                timeout_s=args.timeout_s,
                out_path=args.out,
            )
        )
        return

    fast_path = args.out.with_name("platform_fetch_split_fast.json")
    workday_path = args.out.with_name("platform_fetch_split_workday.json")

    fast = asyncio.run(
        _run(
            platforms={"greenhouse", "ashby", "lever", "oracle_hcm", "icims"},
            concurrency=args.concurrency,
            timeout_s=args.timeout_s,
            out_path=fast_path,
        )
    )
    print("\n--- workday (slower; per-job detail fetch) ---\n", flush=True)
    workday = asyncio.run(
        _run(
            platforms={"workday"},
            concurrency=2,
            timeout_s=args.workday_timeout_s,
            out_path=workday_path,
        )
    )

    merged_results = fast["companies"] + workday["companies"]
    merged = _aggregate(
        merged_results,
        elapsed=fast["elapsed_seconds"] + workday["elapsed_seconds"],
        timeout_s=args.timeout_s,
    )
    merged["parts"] = {"fast": str(fast_path), "workday": str(workday_path)}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    print("\n--- combined ---\n", flush=True)
    _print_summary(merged)
    print(f"\nMerged report: {args.out.resolve()}")


if __name__ == "__main__":
    main()
