from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared import Candidate

PlanTier = Literal["free", "plus", "pro"]

PAST_DUE_GRACE_DAYS = 3
PAID_STATUSES = frozenset({"active", "past_due", "trialing"})


@dataclass(frozen=True)
class TierLimits:
    max_companies: int
    cadence_min_minutes: int
    cadence_max_minutes: int
    delivery: Literal["batched", "instant"]
    default_max_emails_per_day: int
    max_emails_per_day_cap: int
    ats_fit: bool
    hiring_manager: bool
    apply_agent: bool


TIER_LIMITS: dict[PlanTier, TierLimits] = {
    "free": TierLimits(
        max_companies=0,
        cadence_min_minutes=360,
        cadence_max_minutes=720,
        delivery="batched",
        default_max_emails_per_day=3,
        max_emails_per_day_cap=10,
        ats_fit=False,
        hiring_manager=False,
        apply_agent=False,
    ),
    "plus": TierLimits(
        max_companies=25,
        cadence_min_minutes=30,
        cadence_max_minutes=180,
        delivery="batched",
        default_max_emails_per_day=10,
        max_emails_per_day_cap=20,
        ats_fit=True,
        hiring_manager=False,
        apply_agent=False,
    ),
    "pro": TierLimits(
        max_companies=100,
        cadence_min_minutes=15,
        cadence_max_minutes=60,
        delivery="batched",
        default_max_emails_per_day=20,
        max_emails_per_day_cap=50,
        ats_fit=True,
        hiring_manager=True,
        apply_agent=True,
    ),
}

FREE_CADENCE_OPTIONS_MINUTES = [360, 480, 600, 720]
PLUS_CADENCE_OPTIONS_MINUTES = [30, 60, 120, 180]
PRO_CADENCE_OPTIONS_MINUTES = [15, 30, 45, 60]


def normalize_plan_tier(raw: str | None) -> PlanTier:
    if raw == "pro":
        return "pro"
    if raw == "plus":
        return "plus"
    return "free"


def resolve_effective_plan_tier(
    plan_tier: str | None,
    subscription_status: str | None = None,
    plan_expires_at: datetime | None = None,
    *,
    past_due_grace_days: int = PAST_DUE_GRACE_DAYS,
    now: datetime | None = None,
) -> PlanTier:
    raw = normalize_plan_tier(plan_tier)
    if raw == "free":
        return "free"

    status = (subscription_status or "none").strip().lower()
    now = now or datetime.now(timezone.utc)
    expires = plan_expires_at
    if expires is not None and expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if status == "past_due":
        if expires is None:
            return raw
        grace_end = expires + timedelta(days=past_due_grace_days)
        return raw if now <= grace_end else "free"

    if status in PAID_STATUSES:
        if expires is not None and now > expires:
            return "free"
        return raw

    if status == "canceled" and expires is not None and now <= expires:
        return raw

    # Manual comps / legacy rows may set plan_tier without Stripe status.
    if status in ("none", "") and expires is None:
        return raw
    if status in ("none", "") and expires is not None and now <= expires:
        return raw

    return "free"


def get_tier_limits(plan_tier: str | None) -> TierLimits:
    return TIER_LIMITS[normalize_plan_tier(plan_tier)]


def clamp_company_watch_cadence_minutes(minutes: int, plan_tier: str | None) -> int:
    limits = get_tier_limits(plan_tier)
    if limits.max_companies <= 0:
        return limits.cadence_min_minutes
    return max(limits.cadence_min_minutes, min(limits.cadence_max_minutes, minutes))


def clamp_max_emails_per_day(count: int, plan_tier: str | None) -> int:
    limits = get_tier_limits(plan_tier)
    return max(1, min(limits.max_emails_per_day_cap, count))


def default_company_watch_cadence_minutes(plan_tier: str | None) -> int:
    limits = get_tier_limits(plan_tier)
    return limits.cadence_min_minutes


def default_max_emails_per_day(plan_tier: str | None) -> int:
    return get_tier_limits(plan_tier).default_max_emails_per_day


def tier_allows_ats_fit(plan_tier: str | None) -> bool:
    return get_tier_limits(plan_tier).ats_fit


async def get_plan_tier(db: AsyncSession, candidate_id: uuid.UUID) -> PlanTier:
    row = (
        await db.execute(
            select(
                Candidate.plan_tier,
                Candidate.subscription_status,
                Candidate.plan_expires_at,
            ).where(Candidate.id == candidate_id)
        )
    ).one_or_none()
    if row is None:
        return "free"
    return resolve_effective_plan_tier(row.plan_tier, row.subscription_status, row.plan_expires_at)
