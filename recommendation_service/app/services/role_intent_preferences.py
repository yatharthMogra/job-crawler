"""Primary vs pool-derived role_intents on candidate profiles."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from app.constants import DEFAULT_ROLE_INTENTS
from app.models.shared import CandidateProfile
from app.models.subscription import UserPoolSubscription
from app.pool_role_intent import role_intents_for_pools


def primary_role_intents(preferences: dict[str, Any] | None) -> list[str]:
    """Resume/profile-derived role intents — only changed via profile edits."""
    prefs = preferences or {}
    primary = prefs.get("primary_role_intents")
    if isinstance(primary, list) and primary:
        return [str(v) for v in primary if v]
    legacy = prefs.get("role_intents")
    if isinstance(legacy, list) and legacy:
        return [str(v) for v in legacy if v]
    return list(DEFAULT_ROLE_INTENTS)


def pool_derived_role_intents(preferences: dict[str, Any] | None) -> list[str]:
    """Role intents implied by active pool subscriptions."""
    prefs = preferences or {}
    pool_intents = prefs.get("pool_role_intents")
    if isinstance(pool_intents, list):
        return [str(v) for v in pool_intents if v]
    return []


def effective_role_intents(preferences: dict[str, Any] | None) -> list[str]:
    """Union of primary (profile) and pool-derived intents for retrieval filtering."""
    merged: list[str] = []
    seen: set[str] = set()
    for intent in [*primary_role_intents(preferences), *pool_derived_role_intents(preferences)]:
        if intent not in seen:
            seen.add(intent)
            merged.append(intent)
    return merged


async def sync_pool_role_intents(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
) -> list[str]:
    """Recompute pool_role_intents from active subscriptions and persist to current profile."""
    active_pools = list(
        (
            await db.scalars(
                select(UserPoolSubscription.pool_name).where(
                    UserPoolSubscription.candidate_id == candidate_id,
                    UserPoolSubscription.is_active.is_(True),
                )
            )
        ).all()
    )
    intents = role_intents_for_pools(active_pools)

    profile = await db.scalar(
        select(CandidateProfile).where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.is_current.is_(True),
        )
    )
    if profile is None:
        return intents

    preferences = dict(profile.preferences or {})
    preferences["pool_role_intents"] = intents
    profile.preferences = preferences
    flag_modified(profile, "preferences")
    return intents
