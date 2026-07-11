"""In-process hard-constraint evaluation (mirrors build_constraint_filters SQL)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.config import Settings, get_settings
from app.domain import candidate_domains_from_profile
from app.scoring.experience_tier import tiers_above_ceiling
from app.scoring.seniority import (
    get_target_seniority,
    seniority_hard_block_values,
    seniority_retrieval_values,
)
from app.services.profile_loader import UserProfile
from app.services.role_intent_preferences import effective_role_intents


class ConstraintJob(Protocol):
    """Minimal job fields needed for hard-constraint evaluation."""

    id: UUID
    requires_clearance: bool
    sponsorship_status: str
    is_internship: bool
    salary_max: int | None
    role_intent: str | None
    job_domain: str | None
    job_secondary_domain: str | None
    seniority: str
    experience_tier: str


@dataclass
class RankingJob:
    """Skinny job row for RRF ranking + constraint evaluation + score_job."""

    id: UUID
    company_id: UUID
    title: str
    company_name: str
    location: str | None
    job_country: str | None
    posting_url: str | None
    posted_at: datetime | None
    reference_at: datetime | None
    created_at: datetime
    remote_type: str
    application_effort: str | None
    salary_min: int | None
    salary_max: int | None
    opportunity_score: float | None
    retrieval_pools: list[str]
    normalized_roles: list[str]
    job_capabilities: list[str]
    tech_stack: list[str]
    skills: list[str]
    seniority: str
    experience_tier: str
    is_internship: bool
    is_new_grad: bool
    sponsorship_status: str
    sponsorship_confidence: str
    requires_clearance: bool
    requires_citizenship: bool
    role_intent: str | None
    job_domain: str | None
    job_secondary_domain: str | None
    content_embedding: list[float] | None
    responsibilities: list[str] = field(default_factory=list)
    required_qualifications: list[str] = field(default_factory=list)
    preferred_qualifications: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    description_text: str | None = None
    description_preview: str | None = None
    is_active: bool = True
    processing_state: str = "success"
    pool_percentile_cutoffs: dict | None = None


def job_passes_constraints(
    job: ConstraintJob,
    user_profile: UserProfile,
    settings: Settings | None = None,
) -> bool:
    settings = settings or get_settings()
    constraints = user_profile.constraints or {}
    preferences = user_profile.preferences or {}

    if settings.role_intent_filter_enabled:
        role_intents = effective_role_intents(preferences)
        if job.role_intent is None or job.role_intent not in role_intents:
            return False

    if not constraints.get("has_clearance", False) and job.requires_clearance:
        return False

    if settings.domain_filter_enabled:
        candidate_domains = candidate_domains_from_profile(
            user_profile.primary_domain,
            user_profile.secondary_domain,
        )
        if candidate_domains:
            job_domains = {job.job_domain, job.job_secondary_domain} - {None}
            if not job_domains.intersection(candidate_domains):
                return False

    if constraints.get("sponsorship_required"):
        if job.requires_clearance:
            return False
        if job.sponsorship_status == "no":
            return False

    if constraints.get("internship_only") and not job.is_internship:
        return False

    if constraints.get("fulltime_only") and job.is_internship:
        return False

    minimum_salary = constraints.get("minimum_salary")
    if minimum_salary:
        if job.salary_max is not None and job.salary_max < minimum_salary:
            return False

    if settings.experience_tier_visibility_enabled:
        hidden_tiers = tiers_above_ceiling(settings.experience_tier_visibility_ceiling)
        tier = job.experience_tier
        if tier and tier != "UNKNOWN" and tier in hidden_tiers:
            return False
    else:
        target_seniority = get_target_seniority(constraints)
        allowed_values = seniority_retrieval_values(target_seniority)
        if allowed_values and job.seniority not in allowed_values:
            return False
        blocked_values = seniority_hard_block_values(target_seniority)
        if blocked_values and job.seniority is not None and job.seniority in blocked_values:
            return False

    return True


def filter_jobs_by_constraints(
    jobs: list[RankingJob],
    user_profile: UserProfile,
    settings: Settings | None = None,
) -> list[RankingJob]:
    """Preserve input order; drop jobs that fail hard constraints."""
    return [job for job in jobs if job_passes_constraints(job, user_profile, settings)]
