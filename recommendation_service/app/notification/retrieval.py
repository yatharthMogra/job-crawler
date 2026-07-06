from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import and_, not_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.services.role_intent_preferences import effective_role_intents
from app.domain import build_domain_filters, candidate_domains_from_profile
from app.models.notification import NotificationJobHistory
from app.models.shared import NormalizedJob
from app.scoring.experience_tier import tiers_above_ceiling
from app.scoring.seniority import (
    seniority_hard_block_values,
    seniority_retrieval_values,
    get_target_seniority,
)
from app.services.profile_loader import UserProfile


def build_notification_age_filter(settings: Settings) -> list[Any]:
    """Exclude stale postings from notification retrieval."""
    days = settings.job_max_age_days
    if days <= 0:
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return [
        or_(
            NormalizedJob.posted_at >= cutoff,
            and_(
                NormalizedJob.posted_at.is_(None),
                NormalizedJob.created_at >= cutoff,
            ),
        )
    ]


async def fetch_new_jobs_in_pools(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    pools: list[str],
    since: datetime | None,
    limit: int,
    extra_filters: list[Any] | None = None,
    settings: Settings | None = None,
    channel: str = "digest",
) -> list[NormalizedJob]:
    settings = settings or get_settings()
    sent_job_ids = select(NotificationJobHistory.job_id).where(
        NotificationJobHistory.candidate_id == candidate_id,
        NotificationJobHistory.channel == channel,
    )
    conditions = [
        NormalizedJob.retrieval_pools.overlap(pools),
        NormalizedJob.is_active.is_(True),
        NormalizedJob.processing_state == "success",
        NormalizedJob.opportunity_score.is_not(None),
        not_(NormalizedJob.id.in_(sent_job_ids)),
        *build_notification_age_filter(settings),
        *(extra_filters or []),
    ]
    if since is not None:
        conditions.append(NormalizedJob.created_at > since)

    # No opportunity_score pre-filter: all matching jobs feed personalized ranking.
    # `limit` is only a safety cap for unbounded pool growth (not a ranking cutoff).
    stmt = select(NormalizedJob).where(and_(*conditions)).limit(limit)
    return list((await db.scalars(stmt)).all())


def build_constraint_filters(
    user_profile: UserProfile,
    settings: Settings | None = None,
) -> list[Any]:
    """Return SQLAlchemy filter clauses for hard constraints."""
    settings = settings or get_settings()
    filters: list[Any] = []
    constraints = user_profile.constraints or {}
    preferences = user_profile.preferences or {}

    if settings.role_intent_filter_enabled:
        role_intents = effective_role_intents(preferences)
        filters.append(
            and_(
                NormalizedJob.role_intent.isnot(None),
                NormalizedJob.role_intent.in_(role_intents),
            )
        )

    if settings.clearance_filter_enabled and not constraints.get("has_clearance", False):
        filters.append(NormalizedJob.requires_clearance.is_(False))

    if settings.domain_filter_enabled:
        candidate_domains = candidate_domains_from_profile(
            user_profile.primary_domain,
            user_profile.secondary_domain,
        )
        filters.extend(build_domain_filters(candidate_domains))

    if constraints.get("sponsorship_required"):
        # Explicit posting flags only — not inferred H-1B sponsor history.
        filters.append(NormalizedJob.requires_clearance.is_(False))
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

    if settings.experience_tier_visibility_enabled:
        hidden_tiers = tiers_above_ceiling(settings.experience_tier_visibility_ceiling)
        if hidden_tiers:
            filters.append(
                or_(
                    NormalizedJob.experience_tier.is_(None),
                    NormalizedJob.experience_tier == "UNKNOWN",
                    NormalizedJob.experience_tier.notin_(list(hidden_tiers)),
                )
            )
    else:
        target_seniority = get_target_seniority(constraints)
        allowed_values = seniority_retrieval_values(target_seniority)
        if allowed_values:
            filters.append(NormalizedJob.seniority.in_(list(allowed_values)))

        blocked_values = seniority_hard_block_values(target_seniority)
        if blocked_values:
            filters.append(
                or_(
                    NormalizedJob.seniority.is_(None),
                    NormalizedJob.seniority.notin_(list(blocked_values)),
                )
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
