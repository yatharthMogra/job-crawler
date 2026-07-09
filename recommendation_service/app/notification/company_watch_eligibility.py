from __future__ import annotations

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.models.shared import NormalizedJob
from app.notification.filters import job_matches_location_constraints
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile
from app.services.subscriptions import get_active_pools


def job_matches_user_pools(job: NormalizedJob, pools: list[str]) -> bool:
    if not pools:
        return False
    job_pools = job.retrieval_pools or []
    return bool(set(job_pools) & set(pools))


async def job_passes_constraint_filters(
    db: AsyncSession,
    job: NormalizedJob,
    user_profile: UserProfile,
    settings: Settings,
) -> bool:
    filters = build_constraint_filters(user_profile, settings)
    if not filters:
        return True

    stmt = select(func.count()).select_from(NormalizedJob).where(
        and_(NormalizedJob.id == job.id, *filters)
    )
    count = await db.scalar(stmt) or 0
    return count > 0


async def job_passes_company_watch_eligibility(
    db: AsyncSession,
    job: NormalizedJob,
    user_profile: UserProfile,
    settings: Settings | None = None,
    *,
    pools: list[str] | None = None,
) -> bool:
    settings = settings or get_settings()

    if pools is None:
        pools = await get_active_pools(db, user_profile.candidate_id)
    if not job_matches_user_pools(job, pools):
        return False

    if not await job_passes_constraint_filters(db, job, user_profile, settings):
        return False

    return job_matches_location_constraints(job, user_profile)
