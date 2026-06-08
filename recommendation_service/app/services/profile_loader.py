from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared import (
    Candidate,
    CandidateCapability,
    CandidateEvidence,
    CandidateProfile,
)


@dataclass
class UserProfile:
    candidate_id: uuid.UUID
    email: str
    name: str
    constraints: dict[str, Any]
    preferences: dict[str, Any]
    skills: dict[str, Any]
    capabilities: list[CandidateCapability] = field(default_factory=list)
    evidence: list[CandidateEvidence] = field(default_factory=list)


async def load_user_profile(db: AsyncSession, candidate_id: uuid.UUID) -> UserProfile | None:
    candidate = await db.get(Candidate, candidate_id)
    if candidate is None:
        return None

    profile = await db.scalar(
        select(CandidateProfile).where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.is_current.is_(True),
        )
    )
    if profile is None:
        return UserProfile(
            candidate_id=candidate.id,
            email=candidate.email,
            name=candidate.name,
            constraints={},
            preferences={},
            skills={},
        )

    capabilities = (
        await db.scalars(
            select(CandidateCapability).where(
                CandidateCapability.candidate_id == candidate_id,
                CandidateCapability.profile_version == profile.version,
            )
        )
    ).all()
    evidence = (
        await db.scalars(
            select(CandidateEvidence).where(
                CandidateEvidence.candidate_id == candidate_id,
                CandidateEvidence.is_active.is_(True),
                CandidateEvidence.is_approved.is_(True),
            )
        )
    ).all()

    return UserProfile(
        candidate_id=candidate.id,
        email=candidate.email,
        name=candidate.name,
        constraints=profile.constraints or {},
        preferences=profile.preferences or {},
        skills=profile.skills or {},
        capabilities=list(capabilities),
        evidence=list(evidence),
    )
