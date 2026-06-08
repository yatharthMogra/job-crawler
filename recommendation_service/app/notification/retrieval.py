from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import and_, not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import NotificationJobHistory
from app.models.shared import NormalizedJob
from app.services.profile_loader import UserProfile


async def fetch_new_jobs_in_pools(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    pools: list[str],
    since: datetime | None,
    limit: int,
    extra_filters: list[Any] | None = None,
) -> list[NormalizedJob]:
    sent_job_ids = select(NotificationJobHistory.job_id).where(
        NotificationJobHistory.candidate_id == candidate_id
    )
    conditions = [
        NormalizedJob.retrieval_pools.overlap(pools),
        NormalizedJob.is_active.is_(True),
        NormalizedJob.processing_state == "success",
        NormalizedJob.opportunity_score.is_not(None),
        not_(NormalizedJob.id.in_(sent_job_ids)),
        *(extra_filters or []),
    ]
    if since is not None:
        conditions.append(NormalizedJob.created_at > since)

    # No opportunity_score pre-filter: all matching jobs feed personalized ranking.
    # `limit` is only a safety cap for unbounded pool growth (not a ranking cutoff).
    stmt = select(NormalizedJob).where(and_(*conditions)).limit(limit)
    return list((await db.scalars(stmt)).all())


def build_constraint_filters(user_profile: UserProfile) -> list[Any]:
    """Return SQLAlchemy filter clauses for hard constraints."""
    filters: list[Any] = []
    constraints = user_profile.constraints or {}

    if constraints.get("sponsorship_required"):
        filters.append(NormalizedJob.sponsorship_status != "no")

    if constraints.get("internship_only"):
        filters.append(NormalizedJob.is_internship.is_(True))

    if constraints.get("fulltime_only"):
        filters.append(NormalizedJob.is_internship.is_(False))

    minimum_salary = constraints.get("minimum_salary")
    if minimum_salary:
        filters.append(
            (NormalizedJob.salary_max.is_(None)) | (NormalizedJob.salary_max >= minimum_salary)
        )

    return filters


async def query_jobs_in_pools(
    db: AsyncSession,
    *,
    pools: list[str],
    filters: list[Any],
    limit: int,
    offset: int,
) -> list[NormalizedJob]:
    conditions = [
        NormalizedJob.retrieval_pools.overlap(pools),
        NormalizedJob.is_active.is_(True),
        NormalizedJob.processing_state == "success",
        NormalizedJob.opportunity_score.is_not(None),
        *filters,
    ]
    stmt = (
        select(NormalizedJob)
        .where(and_(*conditions))
        .order_by(NormalizedJob.opportunity_score.desc())
        .offset(offset)
        .limit(limit)
    )
    return list((await db.scalars(stmt)).all())
