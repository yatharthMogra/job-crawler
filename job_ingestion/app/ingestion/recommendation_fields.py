from __future__ import annotations

import math
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from app.config import Settings, get_settings

_JOB_ENRICHMENT_RECORD_FIELDS = frozenset(
    {
        "normalized_roles",
        "job_capabilities",
        "application_effort",
        "retrieval_pools",
        "salary_min",
        "salary_max",
        "opportunity_score",
        "opportunity_score_computed_at",
    }
)


def fields_for_job_enrichment_record(recommendation_fields: Mapping[str, Any]) -> dict[str, Any]:
    """Return only keys that map to columns on the job_enrichments audit table."""
    return {key: recommendation_fields[key] for key in _JOB_ENRICHMENT_RECORD_FIELDS if key in recommendation_fields}


def assign_retrieval_pools(
    normalized_roles: list[str],
    is_internship: bool,
    is_new_grad: bool,
) -> list[str]:
    role_type = _resolve_role_type(is_internship, is_new_grad)
    return [f"{role}_{role_type}" for role in normalized_roles]


def assign_validated_retrieval_pools(
    normalized_roles: list[str],
    is_internship: bool,
    is_new_grad: bool,
    job_domain: str,
    job_secondary_domain: str | None = None,
) -> list[str]:
    return assign_retrieval_pools(normalized_roles, is_internship, is_new_grad)


def _resolve_role_type(is_internship: bool, is_new_grad: bool) -> str:
    if is_internship:
        return "INTERNSHIP"
    if is_new_grad:
        return "NEW_GRAD"
    return "FULLTIME"


def compute_opportunity_score(
    reference_at: datetime,
    salary_min: int | None,
    salary_max: int | None,
    application_effort: str | None,
    *,
    settings: Settings | None = None,
) -> float:
    settings = settings or get_settings()
    freshness = _freshness_score(reference_at, decay=settings.opportunity_score_freshness_decay)
    compensation = _compensation_score(
        salary_min,
        salary_max,
        comp_floor=settings.comp_floor,
        comp_ceiling=settings.comp_ceiling,
    )
    effort = settings.effort_scores.get(application_effort or "", 0.5)

    return round(
        settings.freshness_weight * freshness
        + settings.compensation_weight * compensation
        + settings.effort_weight * effort,
        4,
    )


def _freshness_score(reference_at: datetime, *, decay: float) -> float:
    now = datetime.now(timezone.utc)
    if reference_at.tzinfo is None:
        reference_at = reference_at.replace(tzinfo=timezone.utc)
    hours_old = max(0.0, (now - reference_at).total_seconds() / 3600)
    return math.exp(-decay * hours_old)


def _compensation_score(
    salary_min: int | None,
    salary_max: int | None,
    *,
    comp_floor: int,
    comp_ceiling: int,
) -> float:
    if salary_min is None and salary_max is None:
        return 0.5
    if salary_min is not None and salary_max is not None:
        midpoint = (salary_min + salary_max) / 2
    else:
        midpoint = float(salary_min or salary_max or 0)
    clamped = max(comp_floor, min(comp_ceiling, midpoint))
    return (clamped - comp_floor) / (comp_ceiling - comp_floor)
