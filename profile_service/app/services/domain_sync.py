from __future__ import annotations

import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import derive_user_domains
from app.models.capability import CandidateCapability
from app.models.profile import CandidateProfile


async def sync_candidate_domains(db: AsyncSession, candidate_id: uuid.UUID) -> tuple[str, str | None] | None:
    profile = await db.scalar(
        select(CandidateProfile).where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.is_current.is_(True),
        )
    )
    if profile is None:
        return None

    capability_names = list(
        await db.scalars(
            select(CandidateCapability.capability_name).where(
                CandidateCapability.candidate_id == candidate_id,
                CandidateCapability.profile_version == profile.version,
            )
        )
    )
    primary_domain, secondary_domain = derive_user_domains(capability_names)
    await db.execute(
        update(CandidateProfile)
        .where(CandidateProfile.id == profile.id)
        .values(primary_domain=primary_domain, secondary_domain=secondary_domain)
    )
    await db.commit()
    return primary_domain, secondary_domain
