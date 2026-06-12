from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.domain import derive_user_domains
from app.llm.factory import get_llm_provider
from app.models.capability import CandidateCapability
from app.models.evidence import CandidateEvidence
from app.models.profile import CandidateProfile
from app.pipeline.llm_parser import infer_capabilities


def build_evidence_summary(
    evidence: list[CandidateEvidence],
    skills: dict,
) -> str:
    lines: list[str] = ["Skills:"]
    for category, values in skills.items():
        if values:
            lines.append(f"  {category}: {', '.join(values)}")

    lines.append("\nApproved Evidence:")
    for item in evidence:
        if not item.is_approved or not item.is_active:
            continue
        lines.append(f"- {item.evidence_type}: {item.normalized_data}")
    return "\n".join(lines)


async def recompute_capabilities(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    profile_version: int,
    settings: Settings,
) -> list[CandidateCapability]:
    result = await db.execute(
        select(CandidateEvidence).where(
            CandidateEvidence.candidate_id == candidate_id,
            CandidateEvidence.is_approved.is_(True),
            CandidateEvidence.is_active.is_(True),
        )
    )
    evidence = list(result.scalars().all())

    profile_result = await db.execute(
        select(CandidateProfile).where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.version == profile_version,
        )
    )
    profile = profile_result.scalar_one_or_none()
    skills = profile.skills if profile else {}

    summary = build_evidence_summary(evidence, skills)
    llm_provider = get_llm_provider(settings)
    inference = await infer_capabilities(summary, llm_provider)

    await db.execute(delete(CandidateCapability).where(CandidateCapability.candidate_id == candidate_id))

    capabilities: list[CandidateCapability] = []
    for cap in inference.capabilities:
        row = CandidateCapability(
            candidate_id=candidate_id,
            profile_version=profile_version,
            taxonomy_version=settings.capability_taxonomy_version,
            capability_name=cap.name,
            supporting_evidence=cap.supporting_evidence,
            computed_at=datetime.now(UTC),
        )
        db.add(row)
        capabilities.append(row)

    primary_domain, secondary_domain = derive_user_domains([cap.capability_name for cap in capabilities])
    await db.execute(
        update(CandidateProfile)
        .where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.version == profile_version,
        )
        .values(primary_domain=primary_domain, secondary_domain=secondary_domain)
    )
    await db.commit()
    return capabilities
