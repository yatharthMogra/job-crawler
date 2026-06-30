from __future__ import annotations

from typing import Any

import structlog

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.experience_tier import (
    experience_tier_distance_score,
    tiers_above_ceiling,
)
from app.scoring.location import location_alignment_score
from app.scoring.seniority import seniority_score_multiplier
from app.scoring.sponsorship import compute_sponsorship_score
from app.services.h1b_lookup import H1bLookup
from app.services.h1b_pool_family import pool_family_from_roles
from app.services.profile_loader import UserProfile

log = structlog.get_logger(__name__)


def score_job(
    job: NormalizedJob,
    user_profile: UserProfile,
    settings: Settings,
    *,
    h1b_lookup: H1bLookup | None = None,
) -> float:
    cap_score = _capability_overlap(job.job_capabilities, user_profile.capabilities)
    skill_score = _skill_overlap(job.tech_stack + job.skills, user_profile.skills)
    loc_score = _location_alignment(
        job.location,
        job.remote_type,
        user_profile.preferences,
        user_profile.constraints,
        job_country=job.job_country,
        job_title=job.title,
    )
    comp_score = _compensation_alignment(job.salary_min, job.salary_max, user_profile.constraints)

    constraints = user_profile.constraints or {}
    use_tier_scoring = settings.experience_tier_score_enabled
    tier_score = 0.0
    if use_tier_scoring:
        tier_score = experience_tier_distance_score(
            job.experience_tier,
            constraints.get("current_experience_tier"),
        )
    seniority_multiplier = 1.0 if use_tier_scoring else seniority_score_multiplier(
        job.seniority, constraints
    )

    needs_sponsorship = bool(constraints.get("sponsorship_required"))
    use_sponsorship = settings.sponsorship_score_enabled and needs_sponsorship

    if use_sponsorship:
        pool_family = pool_family_from_roles(job.normalized_roles or [])
        sponsorship_score = compute_sponsorship_score(
            job.company_id,
            pool_family,
            needs_sponsorship,
            h1b_lookup,
        )
        base_score = (
            settings.score_capability_weight_with_sponsorship * cap_score
            + settings.score_skill_weight_with_sponsorship * skill_score
            + settings.score_location_weight_with_sponsorship * loc_score
            + settings.score_compensation_weight_with_sponsorship * comp_score
            + settings.score_sponsorship_weight * sponsorship_score
            + (settings.score_experience_tier_weight * tier_score if use_tier_scoring else 0.0)
        )
    elif use_tier_scoring:
        base_score = (
            settings.score_capability_weight_with_tier * cap_score
            + settings.score_skill_weight_with_tier * skill_score
            + settings.score_location_weight_with_tier * loc_score
            + settings.score_compensation_weight_with_tier * comp_score
            + settings.score_experience_tier_weight * tier_score
        )
    else:
        base_score = (
            settings.score_capability_weight * cap_score
            + settings.score_skill_weight * skill_score
            + settings.score_location_weight * loc_score
            + settings.score_compensation_weight * comp_score
        )
    return base_score * seniority_multiplier


def _capability_overlap(job_caps: list[str], user_caps: list[Any]) -> float:
    if not user_caps:
        return 0.0
    user_cap_names = {cap.capability_name for cap in user_caps}
    overlap = len(set(job_caps) & user_cap_names)
    return overlap / len(user_cap_names)


def _flatten_skills(skills: dict[str, Any]) -> list[str]:
    flattened: list[str] = []
    for key in ("languages", "frameworks", "tools", "databases", "other"):
        value = skills.get(key)
        if isinstance(value, list):
            flattened.extend(str(item) for item in value)
    return flattened


def _skill_overlap(job_skills: list[str], user_skills: dict[str, Any]) -> float:
    all_user_skills = _flatten_skills(user_skills)
    if not all_user_skills:
        return 0.0
    job_skills_normalized = {skill.lower() for skill in job_skills}
    user_skills_normalized = {skill.lower() for skill in all_user_skills}
    overlap = len(job_skills_normalized & user_skills_normalized)
    return min(overlap / max(len(user_skills_normalized), 1), 1.0)


def _location_alignment(
    job_location: str | None,
    remote_type: str,
    preferences: dict[str, Any],
    constraints: dict[str, Any],
    *,
    job_country: str | None = None,
    job_title: str | None = None,
) -> float:
    score, matched = location_alignment_score(
        job_location,
        remote_type,
        preferences,
        job_country=job_country,
        constraints=constraints,
    )
    log.debug(
        "location_score",
        job_title=job_title,
        job_location=job_location,
        job_country=job_country,
        remote_type=remote_type,
        preferred_countries=preferences.get("preferred_countries"),
        preferred_locations=preferences.get("preferred_locations"),
        loc_score=score,
        matched_segment=matched,
    )
    return score


def _compensation_alignment(
    salary_min: int | None,
    salary_max: int | None,
    constraints: dict[str, Any],
) -> float:
    minimum_salary = constraints.get("minimum_salary")
    minimum_hourly_rate = constraints.get("minimum_hourly_rate")
    if not minimum_salary and not minimum_hourly_rate:
        return 0.5
    if salary_max is None:
        return 0.5
    if minimum_salary and salary_max >= minimum_salary:
        return 1.0
    return 0.2
