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

from sqlalchemy import and_, func, select, text

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.shared import NormalizedJob
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs
from app.notification.retrieval import build_constraint_filters, query_jobs_in_pools
from app.scoring.explainability import generate_explanations
from app.services.profile_loader import UserProfile, load_user_profile
from app.services.subscriptions import get_active_pools

RECO_BASE = "http://localhost:8002"

ROLE_LABEL_TO_POOL: dict[str, str] = {
    "software engineer": "SWE",
    "software developer": "SWE",
    "python engineer": "SWE",
    "java engineer": "SWE",
    "backend engineer": "BACKEND_ENGINEER",
    "frontend engineer": "FRONTEND_ENGINEER",
    "full stack engineer": "FULLSTACK_ENGINEER",
    "fullstack engineer": "FULLSTACK_ENGINEER",
    "full stack": "FULLSTACK_ENGINEER",
    "ml engineer": "ML_ENGINEER",
    "machine learning engineer": "ML_ENGINEER",
    "ai engineer": "ML_ENGINEER",
    "data engineer": "DATA_ENGINEER",
    "data scientist": "DATA_SCIENTIST",
    "data analyst": "DATA_ANALYST",
    "devops engineer": "DEVOPS_ENGINEER",
    "devops": "DEVOPS_ENGINEER",
    "security engineer": "SECURITY_ENGINEER",
    "mobile engineer": "MOBILE_ENGINEER",
    "solutions engineer": "SOLUTIONS_ENGINEER",
    "support engineer": "SUPPORT_ENGINEER",
    "technical program manager": "TECHNICAL_PROGRAM_MANAGER",
    "product manager": "PRODUCT_MANAGER",
    "product designer": "PRODUCT_DESIGNER",
    "sales": "SALES",
    "customer success": "CUSTOMER_SUCCESS",
    "solutions consultant": "SOLUTIONS_CONSULTANT",
    "partnerships": "PARTNERSHIPS",
    "marketing": "MARKETING",
    "operations": "OPERATIONS",
    "recruiting": "RECRUITING",
    "recruiting / talent": "RECRUITING",
    "finance": "FINANCE",
    "legal": "LEGAL",
    "legal / compliance": "LEGAL",
}

ENGINEERING_POOL_BASES = frozenset(
    {
        "SWE",
        "BACKEND_ENGINEER",
        "FRONTEND_ENGINEER",
        "FULLSTACK_ENGINEER",
        "ML_ENGINEER",
        "DATA_ENGINEER",
        "DATA_SCIENTIST",
        "DEVOPS_ENGINEER",
        "SECURITY_ENGINEER",
        "MOBILE_ENGINEER",
        "SOLUTIONS_ENGINEER",
        "SUPPORT_ENGINEER",
    }
)


def _employment_suffix(constraints: dict) -> str:
    if constraints.get("internship_only"):
        return "INTERNSHIP"
    if constraints.get("new_grad_only"):
        return "NEW_GRAD"
    return "FULLTIME"


def derive_pool_names(profile: UserProfile) -> list[str]:
    prefs = profile.preferences or {}
    constraints = profile.constraints or {}
    suffix = _employment_suffix(constraints)

    explicit = prefs.get("role_pool_ids")
    if isinstance(explicit, list) and explicit:
        return [str(p) for p in explicit]

    pools: set[str] = set()
    for role in (prefs.get("primary_roles") or []) + (prefs.get("secondary_roles") or []):
        if not isinstance(role, str):
            continue
        base = ROLE_LABEL_TO_POOL.get(role.lower().strip())
        if not base:
            continue
        pools.add(f"{base}_{suffix}")
        if base in ENGINEERING_POOL_BASES and base != "SWE":
            pools.add(f"SWE_{suffix}")

    if not pools:
        pools.add(f"SWE_{suffix}")
    return sorted(pools)


async def list_real_users() -> list[dict]:
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                text(
                    """
                    SELECT c.id, c.email, c.name
                    FROM candidates c
                    JOIN candidate_profiles cp
                      ON cp.candidate_id = c.id AND cp.is_current = true
                    WHERE c.email NOT LIKE '%@example.com'
                    ORDER BY c.email
                    """
                )
            )
        ).all()
        return [
            {"candidate_id": str(r.id), "email": r.email, "name": r.name}
            for r in rows
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


async def recommend_for_user(user: dict, *, pools: list[str]) -> dict:
    settings = get_settings()
    candidate_id = uuid.UUID(user["candidate_id"])

    async with AsyncSessionLocal() as db:
        profile = await load_user_profile(db, candidate_id)
        if profile is None:
            raise RuntimeError(f"No profile for {user['email']}")

        filters = build_constraint_filters(profile)

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

        scores = [s for _, s in ranked]
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
            "personal_score_min": round(min(scores), 4) if scores else None,
            "personal_score_max": round(max(scores), 4) if scores else None,
            "personal_score_unique": len({round(s, 4) for s in scores}),
            "notification_top_4": [
                {**_job_row(job, score, generate_explanations(job, profile)), "rank": idx}
                for idx, (job, score) in enumerate(deduped_ranked[:4], start=1)
            ],
            "personalized_ranked_all": personalized,
            "dashboard_by_opportunity_score": dashboard,
        }


async def main() -> None:
    users = await list_real_users()
    if not users:
        raise RuntimeError("No real users with profiles found")

    results = []
    async with httpx.AsyncClient(timeout=120.0) as client:
        for user in users:
            candidate_id = uuid.UUID(user["candidate_id"])
            async with AsyncSessionLocal() as db:
                profile = await load_user_profile(db, candidate_id)
                if profile is None:
                    continue
                derived = derive_pool_names(profile)
                existing = await get_active_pools(db, candidate_id)
                pools = derived if (profile.preferences or {}).get("primary_roles") else (existing or derived)

            await sync_subscriptions(client, user["candidate_id"], pools)
            results.append(await recommend_for_user(user, pools=pools))

    out_json = ROOT / "exports" / "user_recommendations.json"
    out_json.parent.mkdir(exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    summary = {
        u["email"]: {
            "matching_jobs": u["total_matching_jobs"],
            "pools": u["subscribed_pools"],
            "score_range": [u["personal_score_min"], u["personal_score_max"]],
        }
        for u in results
    }
    print(json.dumps(summary, indent=2))
    print(f"wrote {out_json}")


if __name__ == "__main__":
    asyncio.run(main())
