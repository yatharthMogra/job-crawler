#!/usr/bin/env python3
"""Re-queue jobs for targeted domain/pool enrichment fixes (presets 2a–2c, 3a–3h)."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
JOB_INGESTION = ROOT / "job_ingestion"
sys.path.insert(0, str(JOB_INGESTION))

import os

os.chdir(JOB_INGESTION)

from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.ingestion.constants import ProcessingState
from app.ingestion.enrichment_worker import get_enrichment_worker, queue_job_for_enrichment
from app.models.normalized_job import NormalizedJob

PRESET_QUERIES = {
    "2a": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.processing_state = 'success'
          AND (
            ('HARDWARE_ENGINEER' = ANY(nj.normalized_roles)
             AND nj.job_domain NOT IN ('Hardware_Electrical', 'Aerospace_Defense'))
            OR
            ('OPERATIONS' = ANY(nj.normalized_roles) AND nj.job_domain = 'Software')
          )
    """,
    "2b": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Research_Science'
          AND (nj.retrieval_pools IS NULL OR cardinality(nj.retrieval_pools) = 0)
          AND nj.processing_state = 'success'
    """,
    "2c": """
        SELECT nj.id FROM normalized_jobs nj
        JOIN companies c ON c.id = nj.company_id
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Aerospace_Defense'
          AND 'SWE' = ANY(nj.normalized_roles)
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state = 'success'
          AND c.platform IN ('workday', 'oracle_hcm')
    """,
    # Tier 1: secondary-domain + role fixes (prompt v6)
    "3a": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Management'
          AND 'OPERATIONS' = ANY(nj.normalized_roles)
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state IN ('success', 'partial_success')
    """,
    "3b": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Management'
          AND 'TECHNICAL_PROGRAM_MANAGER' = ANY(nj.normalized_roles)
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state IN ('success', 'partial_success')
    """,
    "3c": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Mechanical'
          AND 'HARDWARE_ENGINEER' = ANY(nj.normalized_roles)
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state IN ('success', 'partial_success')
    """,
    "3d": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Hardware_Electrical'
          AND 'SYSTEMS_ENGINEER' = ANY(nj.normalized_roles)
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state IN ('success', 'partial_success')
    """,
    "3e": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Aerospace_Defense'
          AND 'SWE' = ANY(nj.normalized_roles)
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state IN ('success', 'partial_success')
    """,
    "3f": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Software'
          AND 'SYSTEMS_ENGINEER' = ANY(nj.normalized_roles)
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state IN ('success', 'partial_success')
    """,
    "3g": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Industrial_Automation'
          AND cardinality(nj.retrieval_pools) = 0
          AND nj.processing_state IN ('success', 'partial_success')
    """,
    "3h": """
        SELECT nj.id FROM normalized_jobs nj
        WHERE nj.is_active = TRUE
          AND nj.job_domain = 'Hardware_Electrical'
          AND cardinality(nj.retrieval_pools) = 0
          AND (
            nj.title ILIKE '%field service%'
            OR nj.title ILIKE '%field technician%'
          )
          AND nj.processing_state IN ('success', 'partial_success')
    """,
}

TIER1_PRESETS = ["3a", "3b", "3c", "3d", "3e", "3f", "3g", "3h"]
LEGACY_PRESETS = ["2a", "2b", "2c"]
ALL_PRESETS = LEGACY_PRESETS + TIER1_PRESETS


async def collect_job_ids(presets: list[str]) -> list[UUID]:
    ids: set[UUID] = set()
    async with AsyncSessionLocal() as db:
        for preset in presets:
            query = PRESET_QUERIES[preset]
            rows = (await db.execute(text(query))).all()
            for (job_id,) in rows:
                ids.add(UUID(str(job_id)))
            print(f"preset {preset}: {len(rows)} jobs")
    return sorted(ids)


async def requeue(job_ids: list[UUID], source: str) -> int:
    requeued = 0
    async with AsyncSessionLocal() as db:
        for job_id in job_ids:
            job = await db.get(NormalizedJob, job_id)
            if job is None:
                continue
            job.processing_state = ProcessingState.PENDING
            job.failure_reason = None
            job.last_failure_at = None
            await queue_job_for_enrichment(
                db=db,
                normalized_job_id=job_id,
                pipeline_run_id=None,
                source=source,
                priority=1,
            )
            requeued += 1
        await db.commit()
    return requeued


async def main() -> None:
    parser = argparse.ArgumentParser(description="Re-queue jobs for domain fix presets")
    parser.add_argument("--preset", choices=ALL_PRESETS, action="append")
    parser.add_argument("--all", action="store_true", help="Run all presets 2a–2c and 3a–3h")
    parser.add_argument("--tier1", action="store_true", help="Run tier-1 pool fix presets 3a–3h")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.preset:
        presets = args.preset
    elif args.tier1:
        presets = TIER1_PRESETS
    elif args.all:
        presets = ALL_PRESETS
    else:
        presets = []
    if not presets:
        parser.error("Specify --preset or --all")

    job_ids = await collect_job_ids(presets)
    print(f"unique jobs to requeue: {len(job_ids)}")
    if args.dry_run:
        return

    if presets == TIER1_PRESETS:
        source = "taxonomy_tier1"
    elif presets == ALL_PRESETS:
        source = "domain_fix_all"
    elif len(presets) == 1:
        source = f"domain_fix_{presets[0]}"
    else:
        source = "domain_fix_batch"
    requeued = await requeue(job_ids, source=source)
    get_enrichment_worker().wake()
    print(f"requeued {requeued} jobs (job_ingestion worker pool will drain the queue)")


if __name__ == "__main__":
    asyncio.run(main())
