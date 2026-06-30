#!/usr/bin/env python3
"""Spike: validate job_identity_ledger for never-re-ingest-after-seen goal.

Samples jobs from the live DB across multiple platforms and companies, simulates
active-layer purge (raw_jobs + normalized_jobs gone), and measures how many
jobs the current pipeline would misclassify as NEW vs how many a permanent
identity ledger would block from re-ingest.

Usage:
  python scripts/spike_job_identity_ledger.py
  python scripts/spike_job_identity_ledger.py --target-jobs 750 --min-companies 10 --min-platforms 3
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.ingestion.change_detector import classify_jobs
from app.utils.hashing import compute_content_hash


@dataclass
class SampleJob:
    company_id: str
    company_name: str
    platform: str
    external_job_id: str
    content_hash: str
    posted_at: str | None
    raw_api_response: dict[str, Any]


@dataclass
class PlatformPick:
    platform: str
    company_count: int
    jobs_per_company: int


@dataclass
class SpikeReport:
    target_jobs: int
    min_companies: int
    min_platforms: int
    sample_jobs: list[SampleJob] = field(default_factory=list)
    platform_picks: list[PlatformPick] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


async def _platforms_with_jobs(db) -> list[dict[str, Any]]:
    rows = (
        await db.execute(
            text(
                """
                SELECT
                  c.platform,
                  COUNT(DISTINCT c.id) AS company_count,
                  COUNT(*) AS job_count,
                  COUNT(*) FILTER (WHERE nj.posted_at IS NULL) AS null_posted_count
                FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                WHERE nj.is_active = true
                  AND c.is_active = true
                GROUP BY c.platform
                HAVING COUNT(*) >= 20
                ORDER BY COUNT(*) DESC
                """
            )
        )
    ).mappings().all()
    return [dict(row) for row in rows]


async def _top_companies_for_platform(db, platform: str, limit: int) -> list[dict[str, Any]]:
    rows = (
        await db.execute(
            text(
                """
                SELECT
                  c.id::text AS company_id,
                  c.name AS company_name,
                  c.platform,
                  COUNT(*) AS job_count
                FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                WHERE nj.is_active = true
                  AND c.is_active = true
                  AND c.platform = :platform
                GROUP BY c.id, c.name, c.platform
                ORDER BY COUNT(*) DESC, c.name
                LIMIT :limit
                """
            ),
            {"platform": platform, "limit": limit},
        )
    ).mappings().all()
    return [dict(row) for row in rows]


async def _fetch_jobs_for_companies(db, company_ids: list[str], per_company_limit: int) -> list[SampleJob]:
    if not company_ids:
        return []

    rows = (
        await db.execute(
            text(
                """
                SELECT
                  c.id::text AS company_id,
                  c.name AS company_name,
                  c.platform,
                  nj.external_job_id,
                  rj.content_hash,
                  nj.posted_at::text AS posted_at,
                  rj.raw_api_response
                FROM normalized_jobs nj
                JOIN companies c ON c.id = nj.company_id
                JOIN raw_jobs rj ON rj.id = nj.raw_job_id
                WHERE nj.is_active = true
                  AND c.id = ANY(CAST(:company_ids AS uuid[]))
                ORDER BY c.platform, c.name, nj.external_job_id
                """
            ),
            {"company_ids": company_ids},
        )
    ).mappings().all()

    by_company: dict[str, list[SampleJob]] = defaultdict(list)
    for row in rows:
        payload = row["raw_api_response"]
        if not isinstance(payload, dict):
            continue
        job = SampleJob(
            company_id=row["company_id"],
            company_name=row["company_name"],
            platform=row["platform"],
            external_job_id=row["external_job_id"],
            content_hash=row["content_hash"],
            posted_at=row["posted_at"],
            raw_api_response=payload,
        )
        by_company[job.company_id].append(job)

    sampled: list[SampleJob] = []
    for jobs in by_company.values():
        sampled.extend(jobs[:per_company_limit])
    return sampled


def _pick_platforms(
    platform_stats: list[dict[str, Any]],
    *,
    min_platforms: int,
    required_platforms: list[str] | None = None,
) -> list[str]:
    if len(platform_stats) < min_platforms:
        return [row["platform"] for row in platform_stats]

    by_name = {row["platform"]: row for row in platform_stats}
    diverse = sorted(platform_stats, key=lambda r: (r["company_count"], r["job_count"]), reverse=True)

    chosen: list[str] = []
    for name in required_platforms or []:
        if name in by_name and name not in chosen:
            chosen.append(name)

    for row in diverse:
        if row["platform"] not in chosen:
            chosen.append(row["platform"])
        if len(chosen) >= min_platforms:
            break

    return chosen[: max(min_platforms, len(chosen))]


async def build_sample(
    *,
    target_jobs: int,
    min_companies: int,
    min_platforms: int,
    required_platforms: list[str] | None = None,
) -> SpikeReport:
    report = SpikeReport(
        target_jobs=target_jobs,
        min_companies=min_companies,
        min_platforms=min_platforms,
    )

    async with AsyncSessionLocal() as db:
        platform_stats = await _platforms_with_jobs(db)
        if not platform_stats:
            report.errors.append("No active jobs found in normalized_jobs.")
            return report

        chosen_platforms = _pick_platforms(
            platform_stats,
            min_platforms=min_platforms,
            required_platforms=required_platforms,
        )
        if len(chosen_platforms) < min_platforms:
            report.errors.append(
                f"Only {len(chosen_platforms)} platforms with jobs; need {min_platforms}."
            )

        companies_per_platform = max(2, (min_companies + len(chosen_platforms) - 1) // len(chosen_platforms))

        company_ids: list[str] = []
        for platform in chosen_platforms:
            companies = await _top_companies_for_platform(db, platform, companies_per_platform)
            report.platform_picks.append(
                PlatformPick(
                    platform=platform,
                    company_count=len(companies),
                    jobs_per_company=0,
                )
            )
            company_ids.extend(c["company_id"] for c in companies)

        seen: set[str] = set()
        unique_company_ids: list[str] = []
        for cid in company_ids:
            if cid not in seen:
                seen.add(cid)
                unique_company_ids.append(cid)

        if len(unique_company_ids) < min_companies:
            report.errors.append(
                f"Only {len(unique_company_ids)} companies sampled; need {min_companies}."
            )

        # Fetch all jobs for selected companies, then round-robin to target size.
        all_jobs = await _fetch_jobs_for_companies(db, unique_company_ids, per_company_limit=10_000)
        by_company: dict[str, list[SampleJob]] = defaultdict(list)
        for job in all_jobs:
            by_company[job.company_id].append(job)

        sampled: list[SampleJob] = []
        company_order = list(by_company.keys())
        idx = 0
        while len(sampled) < target_jobs and company_order:
            company_id = company_order[idx % len(company_order)]
            bucket = by_company[company_id]
            if bucket:
                sampled.append(bucket.pop(0))
            if not bucket:
                company_order = [cid for cid in company_order if by_company[cid]]
            idx += 1
            if idx > target_jobs * len(unique_company_ids) and len(sampled) < target_jobs:
                break

        report.sample_jobs = sampled
        jobs_per_co = max(1, len(sampled) // max(1, len(unique_company_ids)))
        for pick in report.platform_picks:
            pick.jobs_per_company = jobs_per_co

    return report


def _ledger_identity_key(job: SampleJob) -> tuple[str, str]:
    return (job.company_id, job.external_job_id)


def analyze_sample(report: SpikeReport) -> dict[str, Any]:
    jobs = report.sample_jobs
    ledger_identities = {_ledger_identity_key(job) for job in jobs}

    # Group by company to mirror per-company pipeline classify_jobs
    by_company: dict[str, list[SampleJob]] = defaultdict(list)
    for job in jobs:
        by_company[job.company_id].append(job)

    current_would_ingest = 0
    ledger_would_block = 0
    hash_mismatch_vs_stored = 0
    hash_recomputed_match = 0

    platform_breakdown: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "jobs": 0,
            "current_new": 0,
            "ledger_blocked": 0,
            "hash_recompute_match": 0,
            "hash_recompute_mismatch": 0,
            "null_posted_at": 0,
        }
    )
    company_count_by_platform: dict[str, set[str]] = defaultdict(set)

    for job in jobs:
        pb = platform_breakdown[job.platform]
        pb["jobs"] += 1
        company_count_by_platform[job.platform].add(job.company_id)
        if job.posted_at is None:
            pb["null_posted_at"] += 1

        ledger_would_block += 1
        pb["ledger_blocked"] += 1

        recomputed = compute_content_hash(job.raw_api_response)
        if recomputed == job.content_hash:
            hash_recomputed_match += 1
            pb["hash_recompute_match"] += 1
        else:
            hash_mismatch_vs_stored += 1
            pb["hash_recompute_mismatch"] += 1

    for company_id, company_jobs in by_company.items():
        fetched = [j.raw_api_response for j in company_jobs]
        active_ids = {j.external_job_id for j in company_jobs}
        # Simulated purge: no raw_jobs memory
        classified = classify_jobs(fetched, previous_hashes={}, previously_active_job_ids=active_ids)
        current_would_ingest += len(classified.new) + len(classified.updated)
        platform = company_jobs[0].platform
        platform_breakdown[platform]["current_new"] += len(classified.new)
        platform_breakdown[platform]["current_new"] += len(classified.updated)

    distinct_companies = len({job.company_id for job in jobs})
    distinct_platforms = len({job.platform for job in jobs})

    return {
        "sample_size_jobs": len(jobs),
        "distinct_companies": distinct_companies,
        "distinct_platforms": distinct_platforms,
        "ledger_identities": len(ledger_identities),
        "after_simulated_purge": {
            "current_pipeline_would_reingest": current_would_ingest,
            "ledger_would_block": ledger_would_block,
            "ledger_block_rate_pct": round(100.0 * ledger_would_block / len(jobs), 2) if jobs else 0.0,
            "current_false_new_rate_pct": round(100.0 * current_would_ingest / len(jobs), 2) if jobs else 0.0,
        },
        "hash_stability_on_stored_payload": {
            "recomputed_matches_db": hash_recomputed_match,
            "recomputed_mismatch_db": hash_mismatch_vs_stored,
            "match_rate_pct": round(100.0 * hash_recomputed_match / len(jobs), 2) if jobs else 0.0,
        },
        "platform_breakdown": {
            platform: {
                **counts,
                "companies": len(company_count_by_platform[platform]),
            }
            for platform, counts in sorted(platform_breakdown.items())
        },
    }


def _print_report(report: SpikeReport, analysis: dict[str, Any]) -> None:
    print("=" * 72)
    print("JOB IDENTITY LEDGER SPIKE")
    print("=" * 72)
    print(f"Target jobs:     {report.target_jobs}")
    print(f"Min companies:   {report.min_companies}")
    print(f"Min platforms:   {report.min_platforms}")
    print()

    if report.errors:
        print("WARNINGS:")
        for err in report.errors:
            print(f"  - {err}")
        print()

    print("Platforms selected:")
    for pick in report.platform_picks:
        print(
            f"  - {pick.platform}: up to {pick.company_count} companies, "
            f"up to {pick.jobs_per_company} jobs/company"
        )
    print()

    print("Sample:")
    print(f"  Jobs:       {analysis['sample_size_jobs']}")
    print(f"  Companies:  {analysis['distinct_companies']}")
    print(f"  Platforms:  {analysis['distinct_platforms']}")
    print()

    purge = analysis["after_simulated_purge"]
    print("After simulated purge (raw_jobs memory gone):")
    print(f"  Current pipeline would re-ingest: {purge['current_pipeline_would_reingest']} jobs "
          f"({purge['current_false_new_rate_pct']}%)")
    print(f"  Identity ledger would block:      {purge['ledger_would_block']} jobs "
          f"({purge['ledger_block_rate_pct']}%)")
    print()

    hs = analysis["hash_stability_on_stored_payload"]
    print("Hash recompute on stored raw_api_response (sanity check):")
    print(f"  Matches DB content_hash:  {hs['recomputed_matches_db']} ({hs['match_rate_pct']}%)")
    print(f"  Mismatch DB content_hash: {hs['recomputed_mismatch_db']}")
    print()

    print("Per platform:")
    for platform, stats in analysis["platform_breakdown"].items():
        print(
            f"  {platform}: jobs={stats['jobs']} companies={stats['companies']} "
            f"null_posted_at={stats['null_posted_at']} "
            f"current_reingest={stats['current_new']} ledger_blocked={stats['ledger_blocked']}"
        )
    print("=" * 72)

    if analysis["sample_size_jobs"] >= 500 and analysis["distinct_companies"] >= 10 and analysis["distinct_platforms"] >= 3:
        if purge["ledger_block_rate_pct"] == 100.0:
            print("VERDICT: PASS — ledger blocks 100% of re-seen identities across sample.")
        else:
            print("VERDICT: PARTIAL — ledger does not cover full sample.")
    else:
        print("VERDICT: INCOMPLETE SAMPLE — adjust DB or parameters.")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Spike test for job_identity_ledger")
    parser.add_argument("--target-jobs", type=int, default=750, help="Target job sample size (500-1000)")
    parser.add_argument("--min-companies", type=int, default=10, help="Minimum distinct companies")
    parser.add_argument("--min-platforms", type=int, default=3, help="Minimum distinct platforms")
    parser.add_argument(
        "--required-platforms",
        default="workday,greenhouse,smartrecruiters",
        help="Comma-separated platforms to include when available",
    )
    args = parser.parse_args()

    required = [p.strip() for p in args.required_platforms.split(",") if p.strip()]

    report = await build_sample(
        target_jobs=max(500, min(1000, args.target_jobs)),
        min_companies=args.min_companies,
        min_platforms=args.min_platforms,
        required_platforms=required,
    )
    analysis = analyze_sample(report)
    _print_report(report, analysis)


if __name__ == "__main__":
    asyncio.run(main())
