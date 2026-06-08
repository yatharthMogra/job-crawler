#!/usr/bin/env python3
"""Run full dashboard + personalized recommendations for real users."""

from __future__ import annotations

import asyncio
import json
import sys
import uuid
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "recommendation_service"))

from sqlalchemy import and_, func, select

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.shared import NormalizedJob
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs
from app.notification.retrieval import build_constraint_filters, query_jobs_in_pools
from app.scoring.explainability import generate_explanations
from app.services.profile_loader import load_user_profile
from app.services.subscriptions import get_active_pools

RECO_BASE = "http://localhost:8002"

USERS = [
    {
        "email": "yatharthmogra@gmail.com",
        "candidate_id": "6230dd88-b346-4e96-94fd-4a51c4500f34",
        "pools": [
            "SWE_FULLTIME",
            "BACKEND_ENGINEER_FULLTIME",
            "ML_ENGINEER_FULLTIME",
            "FULLSTACK_ENGINEER_FULLTIME",
        ],
    },
    {
        "email": "ramparekh208@gmail.com",
        "candidate_id": "9502535f-33c7-452e-8fb4-bf3467eb8394",
        "pools": [
            "DATA_ENGINEER_FULLTIME",
            "DATA_SCIENTIST_FULLTIME",
            "ML_ENGINEER_FULLTIME",
            "SWE_FULLTIME",
        ],
    },
]


def _job_row(job: NormalizedJob, personal_score: float | None, explanations: list[str] | None) -> dict:
    return {
        "rank": None,
        "job_id": str(job.id),
        "title": job.title,
        "company": job.company_name,
        "location": job.location,
        "remote_type": job.remote_type,
        "posted_at": job.posted_at.isoformat() if job.posted_at else None,
        "posting_url": job.posting_url,
        "opportunity_score": job.opportunity_score,
        "personal_score": round(personal_score, 4) if personal_score is not None else None,
        "application_effort": job.application_effort,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "retrieval_pools": job.retrieval_pools,
        "normalized_roles": job.normalized_roles,
        "job_capabilities": job.job_capabilities,
        "tech_stack": job.tech_stack[:8],
        "skills": job.skills[:8],
        "match_reasons": explanations or [],
    }


async def sync_subscriptions(client: httpx.AsyncClient, candidate_id: str, pools: list[str]) -> None:
    resp = await client.patch(
        f"{RECO_BASE}/subscriptions/{candidate_id}",
        json={"pool_names": pools, "is_active": True},
    )
    resp.raise_for_status()


async def recommend_for_user(user: dict) -> dict:
    settings = get_settings()
    candidate_id = uuid.UUID(user["candidate_id"])

    async with AsyncSessionLocal() as db:
        profile = await load_user_profile(db, candidate_id)
        if profile is None:
            raise RuntimeError(f"No profile for {user['email']}")

        pools = await get_active_pools(db, candidate_id)
        filters = build_constraint_filters(profile)

        # Fetch all matching jobs (paginate in chunks of 200)
        all_jobs: list[NormalizedJob] = []
        offset = 0
        while True:
            chunk = await query_jobs_in_pools(
                db, pools=pools, filters=filters, limit=200, offset=offset
            )
            if not chunk:
                break
            all_jobs.extend(chunk)
            if len(chunk) < 200:
                break
            offset += 200

        count_stmt = select(func.count()).select_from(NormalizedJob).where(
            and_(
                NormalizedJob.retrieval_pools.overlap(pools),
                NormalizedJob.is_active.is_(True),
                NormalizedJob.processing_state == "success",
                NormalizedJob.opportunity_score.is_not(None),
                *filters,
            )
        )
        total = await db.scalar(count_stmt) or 0

        pool_breakdown = await db.execute(
            select(
                func.unnest(NormalizedJob.retrieval_pools).label("pool"),
                func.count().label("jobs"),
            )
            .where(
                and_(
                    NormalizedJob.retrieval_pools.overlap(pools),
                    NormalizedJob.is_active.is_(True),
                    NormalizedJob.processing_state == "success",
                    NormalizedJob.opportunity_score.is_not(None),
                    *filters,
                )
            )
            .group_by("pool")
            .order_by(func.count().desc())
        )

        ranked = rank_jobs(all_jobs, profile, settings)
        deduped_ranked = deduplicate_ranked_jobs(ranked)
        dashboard_sorted = sorted(all_jobs, key=lambda j: j.opportunity_score or 0, reverse=True)

        personalized = []
        for idx, (job, score) in enumerate(ranked, start=1):
            row = _job_row(job, score, generate_explanations(job, profile))
            row["rank"] = idx
            personalized.append(row)

        dashboard = []
        for idx, job in enumerate(dashboard_sorted, start=1):
            score = next((s for j, s in ranked if j.id == job.id), None)
            row = _job_row(job, score, generate_explanations(job, profile))
            row["rank"] = idx
            dashboard.append(row)

        return {
            "email": user["email"],
            "candidate_id": user["candidate_id"],
            "name": profile.name,
            "subscribed_pools": pools,
            "constraints": profile.constraints,
            "preferences": profile.preferences,
            "capabilities": [c.capability_name for c in profile.capabilities],
            "total_matching_jobs": total,
            "pool_breakdown": [dict(r._mapping) for r in pool_breakdown],
            "notification_top_4": [
                {**_job_row(job, score, generate_explanations(job, profile)), "rank": idx}
                for idx, (job, score) in enumerate(deduped_ranked[:4], start=1)
            ],
            "personalized_ranked_all": personalized,
            "dashboard_by_opportunity_score": dashboard,
        }


async def main() -> None:
    results = []
    async with httpx.AsyncClient(timeout=60.0) as client:
        for user in USERS:
            await sync_subscriptions(client, user["candidate_id"], user["pools"])
            results.append(await recommend_for_user(user))

    out_json = ROOT / "exports" / "user_recommendations.json"
    out_json.parent.mkdir(exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(json.dumps({u["email"]: u["total_matching_jobs"] for u in results}, indent=2))
    print(f"wrote {out_json}")


if __name__ == "__main__":
    asyncio.run(main())
