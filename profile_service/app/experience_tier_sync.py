from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.experience_tier import (
    derive_current_experience_tier,
    evidence_months_to_years,
    sum_evidence_months,
)
from app.models.evidence import CandidateEvidence


def _parse_graduation_month(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    parts = cleaned.split("-")
    try:
        if len(parts) >= 2:
            return datetime(int(parts[0]), int(parts[1]), 1, tzinfo=UTC)
        if len(parts) == 1 and parts[0].isdigit():
            return datetime(int(parts[0]), 12, 31, tzinfo=UTC)
    except ValueError:
        return None
    return None


def infer_is_currently_enrolled(education: dict[str, Any]) -> bool | None:
    explicit = education.get("is_currently_enrolled")
    if isinstance(explicit, bool):
        return explicit
    now = datetime.now(UTC)
    entries = education.get("entries")
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            grad = _parse_graduation_month(str(entry.get("graduation_date") or ""))
            if grad is not None and grad > now:
                return True
    grad = _parse_graduation_month(str(education.get("graduation_date") or ""))
    if grad is not None and grad > now:
        return True
    return None


async def load_approved_experience_months(db: AsyncSession, candidate_id: uuid.UUID) -> int:
    rows = (
        await db.scalars(
            select(CandidateEvidence).where(
                CandidateEvidence.candidate_id == candidate_id,
                CandidateEvidence.is_active.is_(True),
                CandidateEvidence.is_approved.is_(True),
                CandidateEvidence.evidence_type == "experience",
            )
        )
    ).all()
    return sum_evidence_months(rows)


async def refresh_experience_tier_constraints(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    constraints: dict[str, Any],
    education: dict[str, Any],
) -> dict[str, Any]:
    evidence_months = await load_approved_experience_months(db, candidate_id)
    full_time_years = constraints.get("full_time_experience_years")
    if full_time_years is None and evidence_months > 0:
        full_time_years = evidence_months_to_years(evidence_months)

    enrolled = constraints.get("is_currently_enrolled")
    if enrolled is None:
        enrolled = infer_is_currently_enrolled(education)

    tier = derive_current_experience_tier(
        full_time_years=float(full_time_years) if full_time_years is not None else None,
        is_currently_enrolled=enrolled,
        expected_graduation=constraints.get("expected_graduation_date"),
        evidence_months=evidence_months,
        internship_only=bool(constraints.get("internship_only")),
    )

    updated = dict(constraints)
    if full_time_years is not None:
        updated["full_time_experience_years"] = float(full_time_years)
    if enrolled is not None:
        updated["is_currently_enrolled"] = bool(enrolled)
    updated["current_experience_tier"] = tier
    return updated
