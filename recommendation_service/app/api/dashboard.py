from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.shared import NormalizedJob
from app.notification.retrieval import build_constraint_filters, query_jobs_in_pools
from app.schemas.dashboard import DashboardJobOut, DashboardJobsResponse
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

    user_profile = await load_user_profile(db, candidate_id)
    filters = build_constraint_filters(user_profile) if user_profile else []

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
