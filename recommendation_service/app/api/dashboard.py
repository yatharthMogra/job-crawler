from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database import get_db
from app.models.shared import NormalizedJob
from app.notification.ranker import deduplicate_ranked_jobs, rank_jobs
from app.notification.retrieval import build_constraint_filters, query_jobs_in_pools
from app.scoring.explainability import generate_explanations
from app.schemas.applications import (
    UserApplicationOut,
    UserApplicationPatchIn,
    UserApplicationsResponse,
)
from app.schemas.dashboard import (
    DashboardJobOut,
    DashboardJobsResponse,
    DashboardRecommendedJobOut,
    DashboardRecommendedJobsResponse,
)
from app.services.applications import apply_to_job, get_user_applications, patch_application
from app.services.profile_loader import load_user_profile
from app.services.subscriptions import get_active_pools

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _job_to_out(job: NormalizedJob) -> DashboardJobOut:
    return DashboardJobOut(
        id=job.id,
        title=job.title,
        company_name=job.company_name,
        location=job.location,
        posting_url=job.posting_url,
        posted_at=job.posted_at,
        remote_type=job.remote_type,
        application_effort=job.application_effort,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        opportunity_score=job.opportunity_score,
        retrieval_pools=job.retrieval_pools,
        normalized_roles=job.normalized_roles,
        job_capabilities=job.job_capabilities,
        tech_stack=job.tech_stack,
        skills=job.skills,
        seniority=job.seniority,
    )


@router.get("/jobs", response_model=DashboardJobsResponse)
async def get_dashboard_jobs(
    candidate_id: uuid.UUID = Query(...),
    location: Optional[str] = Query(default=None),
    remote_type: Optional[str] = Query(default=None),
    salary_min: Optional[int] = Query(default=None),
    role_type: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> DashboardJobsResponse:
    pools = await get_active_pools(db, candidate_id)
    if not pools:
        return DashboardJobsResponse(jobs=[], total=0)

    settings = get_settings()
    user_profile = await load_user_profile(db, candidate_id)
    filters = build_constraint_filters(user_profile, settings) if user_profile else []

    if location:
        filters.append(NormalizedJob.location.ilike(f"%{location}%"))
    if remote_type:
        filters.append(NormalizedJob.remote_type == remote_type)
    if salary_min is not None:
        filters.append(or_(NormalizedJob.salary_min.is_(None), NormalizedJob.salary_min >= salary_min))
    if role_type:
        suffix = f"_{role_type.upper()}"
        matching_pools = [pool for pool in pools if pool.endswith(suffix)]
        if matching_pools:
            filters.append(NormalizedJob.retrieval_pools.overlap(matching_pools))

    jobs = await query_jobs_in_pools(
        db,
        pools=pools,
        filters=filters,
        limit=limit,
        offset=offset,
    )

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
    return DashboardJobsResponse(jobs=[_job_to_out(job) for job in jobs], total=total)


async def _fetch_all_pool_jobs(
    db: AsyncSession,
    *,
    pools: list[str],
    filters: list,
    cap: int,
) -> list[NormalizedJob]:
    all_jobs: list[NormalizedJob] = []
    offset = 0
    while len(all_jobs) < cap:
        chunk = await query_jobs_in_pools(
            db, pools=pools, filters=filters, limit=min(200, cap - len(all_jobs)), offset=offset
        )
        if not chunk:
            break
        all_jobs.extend(chunk)
        offset += len(chunk)
        if len(chunk) < 200:
            break
    return all_jobs


@router.get("/jobs/recommended", response_model=DashboardRecommendedJobsResponse)
async def get_recommended_jobs(
    candidate_id: uuid.UUID = Query(...),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> DashboardRecommendedJobsResponse:
    pools = await get_active_pools(db, candidate_id)
    if not pools:
        return DashboardRecommendedJobsResponse(jobs=[], total=0)

    user_profile = await load_user_profile(db, candidate_id)
    if user_profile is None:
        return DashboardRecommendedJobsResponse(jobs=[], total=0)

    filters = build_constraint_filters(user_profile, settings)
    cap = settings.notification_retrieval_limit
    all_jobs = await _fetch_all_pool_jobs(db, pools=pools, filters=filters, cap=cap)
    ranked = deduplicate_ranked_jobs(rank_jobs(all_jobs, user_profile, settings))
    total = len(ranked)
    page = ranked[offset : offset + limit]

    jobs_out: list[DashboardRecommendedJobOut] = []
    for job, score in page:
        base = _job_to_out(job)
        jobs_out.append(
            DashboardRecommendedJobOut(
                **base.model_dump(),
                personal_score=score,
                match_reasons=generate_explanations(job, user_profile),
            )
        )
    return DashboardRecommendedJobsResponse(jobs=jobs_out, total=total)


@router.get("/jobs/{job_id}", response_model=DashboardJobOut)
async def get_dashboard_job(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> DashboardJobOut:
    pools = await get_active_pools(db, candidate_id)
    if not pools:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active subscriptions")

    job = await db.scalar(
        select(NormalizedJob).where(
            NormalizedJob.id == job_id,
            NormalizedJob.retrieval_pools.overlap(pools),
            NormalizedJob.is_active.is_(True),
            NormalizedJob.processing_state == "success",
        )
    )
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return _job_to_out(job)


@router.post("/jobs/{job_id}/apply", response_model=UserApplicationOut)
async def mark_job_applied(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> UserApplicationOut:
    return await apply_to_job(db, candidate_id=candidate_id, job_id=job_id)


@router.get("/applications", response_model=UserApplicationsResponse)
async def list_applications(
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> UserApplicationsResponse:
    applications = await get_user_applications(db, candidate_id)
    return UserApplicationsResponse(applications=applications, total=len(applications))


@router.patch("/applications/{application_id}", response_model=UserApplicationOut)
async def update_application(
    application_id: uuid.UUID,
    payload: UserApplicationPatchIn,
    candidate_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> UserApplicationOut:
    return await patch_application(
        db,
        candidate_id=candidate_id,
        application_id=application_id,
        payload=payload,
    )
