from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared import Candidate

PlanTier = Literal["free", "plus"]


@dataclass(frozen=True)
class TierLimits:
    max_companies: int
    cadence_min_minutes: int
    cadence_max_minutes: int
    delivery: Literal["batched", "instant"]
    default_max_emails_per_day: int
    max_emails_per_day_cap: int


TIER_LIMITS: dict[PlanTier, TierLimits] = {
    "free": TierLimits(
        max_companies=5,
        cadence_min_minutes=360,
        cadence_max_minutes=720,
        delivery="batched",
        default_max_emails_per_day=3,
        max_emails_per_day_cap=10,
    ),
    "plus": TierLimits(
        max_companies=25,
        cadence_min_minutes=30,
        cadence_max_minutes=180,
        delivery="batched",
        default_max_emails_per_day=10,
        max_emails_per_day_cap=20,
    ),
}

FREE_CADENCE_OPTIONS_MINUTES = [360, 480, 600, 720]
PLUS_CADENCE_OPTIONS_MINUTES = [30, 60, 120, 180]


def normalize_plan_tier(raw: str | None) -> PlanTier:
    if raw == "plus":
        return "plus"
    return "free"


def get_tier_limits(plan_tier: str | None) -> TierLimits:
    return TIER_LIMITS[normalize_plan_tier(plan_tier)]


def clamp_company_watch_cadence_minutes(minutes: int, plan_tier: str | None) -> int:
    limits = get_tier_limits(plan_tier)
    return max(limits.cadence_min_minutes, min(limits.cadence_max_minutes, minutes))


def clamp_max_emails_per_day(count: int, plan_tier: str | None) -> int:
    limits = get_tier_limits(plan_tier)
    return max(1, min(limits.max_emails_per_day_cap, count))


def default_company_watch_cadence_minutes(plan_tier: str | None) -> int:
    limits = get_tier_limits(plan_tier)
    return limits.cadence_min_minutes


def default_max_emails_per_day(plan_tier: str | None) -> int:
    return get_tier_limits(plan_tier).default_max_emails_per_day


async def get_plan_tier(db: AsyncSession, candidate_id: uuid.UUID) -> PlanTier:
    tier = await db.scalar(select(Candidate.plan_tier).where(Candidate.id == candidate_id))
    return normalize_plan_tier(tier)
