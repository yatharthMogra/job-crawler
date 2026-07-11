from __future__ import annotations

import math
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

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
    return [NormalizedJob.reference_at >= cutoff]


def pool_floor_size(cap: int, num_pools: int, ratio: float) -> int:
    if num_pools <= 0:
        return cap
    return max(1, math.ceil((cap / num_pools) * ratio))


def _base_pool_conditions(pools: list[str], filters: list[Any]) -> list[Any]:
    return [
        NormalizedJob.retrieval_pools.overlap(pools),
        NormalizedJob.is_active.is_(True),
        NormalizedJob.processing_state == "success",
        NormalizedJob.opportunity_score.is_not(None),
        *filters,
    ]


async def query_jobs_in_single_pool(
    db: AsyncSession,
    *,
    pool: str,
    filters: list[Any],
    limit: int,
    exclude_ids: set[UUID] | None = None,
) -> list[NormalizedJob]:
    conditions = [
        NormalizedJob.retrieval_pools.contains([pool]),
        NormalizedJob.is_active.is_(True),
        NormalizedJob.processing_state == "success",
        NormalizedJob.opportunity_score.is_not(None),
        *filters,
    ]
    if exclude_ids:
        conditions.append(NormalizedJob.id.notin_(list(exclude_ids)))
    stmt = (
        select(NormalizedJob)
        .where(and_(*conditions))
        .order_by(NormalizedJob.opportunity_score.desc())
        .limit(limit)
    )
    return list((await db.scalars(stmt)).all())


async def fetch_jobs_with_pool_floors(
    db: AsyncSession,
    *,
    pools: list[str],
    filters: list[Any],
    cap: int,
    floor_ratio: float,
) -> list[NormalizedJob]:
    if not pools or cap <= 0:
        return []

    selected: list[NormalizedJob] = []
    selected_ids: set[UUID] = set()
    min_per_pool = pool_floor_size(cap, len(pools), floor_ratio)

    for pool in pools:
        if len(selected) >= cap:
            break
        chunk = await query_jobs_in_single_pool(
            db,
            pool=pool,
            filters=filters,
            limit=min_per_pool,
            exclude_ids=selected_ids,
        )
        for job in chunk:
            if job.id in selected_ids:
                continue
            selected_ids.add(job.id)
            selected.append(job)
            if len(selected) >= cap:
                break

    remaining = cap - len(selected)
    if remaining <= 0:
        return selected

    offset = 0
    while len(selected) < cap:
        chunk_limit = min(200, cap - len(selected))
        chunk = await query_jobs_in_pools(
            db,
            pools=pools,
            filters=filters,
            limit=chunk_limit,
            offset=offset,
            exclude_ids=selected_ids,
        )
        if not chunk:
            break
        for job in chunk:
            if job.id in selected_ids:
                continue
            selected_ids.add(job.id)
            selected.append(job)
            if len(selected) >= cap:
                break
        offset += len(chunk)
        if len(chunk) < chunk_limit:
            break

    return selected


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

    if not constraints.get("has_clearance", False):
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
    exclude_ids: set[UUID] | None = None,
) -> list[NormalizedJob]:
    conditions = _base_pool_conditions(pools, filters)
    if exclude_ids:
        conditions.append(NormalizedJob.id.notin_(list(exclude_ids)))
    stmt = (
        select(NormalizedJob)
        .where(and_(*conditions))
        .order_by(NormalizedJob.opportunity_score.desc())
        .offset(offset)
        .limit(limit)
    )
    return list((await db.scalars(stmt)).all())


# Columns needed for RRF + constraints + score_job — exclude description_text/preview.
_RANKING_LOAD_ONLY = (
    NormalizedJob.id,
    NormalizedJob.company_id,
    NormalizedJob.title,
    NormalizedJob.company_name,
    NormalizedJob.location,
    NormalizedJob.job_country,
    NormalizedJob.posting_url,
    NormalizedJob.posted_at,
    NormalizedJob.reference_at,
    NormalizedJob.created_at,
    NormalizedJob.remote_type,
    NormalizedJob.application_effort,
    NormalizedJob.salary_min,
    NormalizedJob.salary_max,
    NormalizedJob.opportunity_score,
    NormalizedJob.retrieval_pools,
    NormalizedJob.normalized_roles,
    NormalizedJob.job_capabilities,
    NormalizedJob.tech_stack,
    NormalizedJob.skills,
    NormalizedJob.required_skills,
    NormalizedJob.preferred_skills,
    NormalizedJob.seniority,
    NormalizedJob.experience_tier,
    NormalizedJob.is_internship,
    NormalizedJob.is_new_grad,
    NormalizedJob.sponsorship_status,
    NormalizedJob.sponsorship_confidence,
    NormalizedJob.requires_clearance,
    NormalizedJob.requires_citizenship,
    NormalizedJob.role_intent,
    NormalizedJob.job_domain,
    NormalizedJob.job_secondary_domain,
    NormalizedJob.content_embedding,
    NormalizedJob.responsibilities,
    NormalizedJob.required_qualifications,
    NormalizedJob.preferred_qualifications,
    NormalizedJob.benefits,
    NormalizedJob.is_active,
    NormalizedJob.processing_state,
)


async def query_jobs_for_ranking(
    db: AsyncSession,
    *,
    pools: list[str],
    settings: Settings | None = None,
) -> list[NormalizedJob]:
    """Pool-matched skinny retrieval for RRF — no hard constraints, no description text.

    Freshness bound uses JOB_MAX_AGE_DAYS (same window as active-job archival).
    """
    from sqlalchemy.orm import load_only

    settings = settings or get_settings()
    conditions = [
        NormalizedJob.retrieval_pools.overlap(pools),
        NormalizedJob.is_active.is_(True),
        NormalizedJob.processing_state == "success",
        NormalizedJob.opportunity_score.is_not(None),
        *build_notification_age_filter(settings),
    ]
    stmt = (
        select(NormalizedJob)
        .options(load_only(*_RANKING_LOAD_ONLY))
        .where(and_(*conditions))
        .order_by(NormalizedJob.opportunity_score.desc())
    )
    return list((await db.scalars(stmt)).all())
