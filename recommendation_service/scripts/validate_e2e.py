"""Validate recommendation pipeline end-to-end against live database."""

from __future__ import annotations

import asyncio
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INGESTION_ROOT = ROOT / "job_ingestion"
RECO_ROOT = ROOT / "recommendation_service"


async def run_ingestion_validation() -> tuple[int, uuid.UUID | None, str | None]:
    sys.path.insert(0, str(INGESTION_ROOT))
    from app.config import get_settings
    from app.database import AsyncSessionLocal
    from app.ingestion.recommendation_fields import assign_retrieval_pools, compute_opportunity_score
    from app.ingestion.reprocessor import reprocess_jobs
    from app.models.normalized_job import NormalizedJob
    from app.schemas.reprocessing import ReprocessingFilters
    from sqlalchemy import select, text

    settings = get_settings()
    async with AsyncSessionLocal() as db:
        result = await reprocess_jobs(
            db=db,
            settings=settings,
            filters=ReprocessingFilters(processing_state=["success"]),
            target_version="v2",
            dry_run=True,
        )
        print(f"dry_run matched_jobs={result.matched_jobs}")

        jobs = (
            await db.scalars(
                select(NormalizedJob)
                .where(
                    NormalizedJob.processing_state == "success",
                    NormalizedJob.opportunity_score.is_(None),
                )
                .limit(25)
            )
        ).all()
        for job in jobs:
            roles = ["SWE"] if "engineer" in job.title.lower() else ["OTHER"]
            if "ml" in job.title.lower() or "machine learning" in job.title.lower():
                roles = ["ML_ENGINEER"]
            caps = ["Backend Engineering"] if "backend" in job.title.lower() else []
            effort = "MEDIUM"
            job.normalized_roles = roles
            job.job_capabilities = caps
            job.application_effort = effort
            job.retrieval_pools = assign_retrieval_pools(roles, job.is_internship, job.is_new_grad)
            job.opportunity_score = compute_opportunity_score(
                job.reference_at or job.posted_at or job.created_at,
                job.salary_min,
                job.salary_max,
                effort,
                settings=settings,
            )
            job.opportunity_score_computed_at = job.extracted_at
        await db.commit()
        print(f"backfilled_jobs={len(jobs)}")

        candidate_id = await db.scalar(text("SELECT id FROM candidates LIMIT 1"))
        sample_pool = jobs[0].retrieval_pools[0] if jobs and jobs[0].retrieval_pools else "SWE_FULLTIME"
        return len(jobs), candidate_id, sample_pool


async def run_reco_validation(candidate_id: uuid.UUID, sample_pool: str) -> None:
    for key in list(sys.modules):
        if key == "app" or key.startswith("app."):
            del sys.modules[key]
    if str(RECO_ROOT) not in sys.path:
        sys.path.insert(0, str(RECO_ROOT))

    from sqlalchemy import select

    from app.database import AsyncSessionLocal
    from app.models.subscription import UserPoolSubscription
    from app.notification.retrieval import query_jobs_in_pools
    from app.services.subscriptions import get_active_pools

    async with AsyncSessionLocal() as db:
        existing = await db.scalar(
            select(UserPoolSubscription).where(
                UserPoolSubscription.candidate_id == candidate_id,
                UserPoolSubscription.pool_name == sample_pool,
            )
        )
        if existing is None:
            db.add(
                UserPoolSubscription(
                    candidate_id=candidate_id,
                    pool_name=sample_pool,
                    is_active=True,
                )
            )
            await db.commit()
        print(f"subscribed candidate to pool={sample_pool}")

        pools = await get_active_pools(db, candidate_id)
        jobs = await query_jobs_in_pools(db, pools=pools, filters=[], limit=10, offset=0)
        print(f"dashboard_jobs={len(jobs)} pools={pools}")
        assert len(jobs) > 0


async def main() -> None:
    backfilled, candidate_id, sample_pool = await run_ingestion_validation()
    if candidate_id is None or backfilled == 0 or sample_pool is None:
        print("Skipping reco validation — missing candidate or backfilled jobs")
        return
    await run_reco_validation(candidate_id, sample_pool)
    print("e2e validation complete")


if __name__ == "__main__":
    asyncio.run(main())
