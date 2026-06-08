from __future__ import annotations

from typing import Any

from app.config import Settings
from app.models.shared import NormalizedJob
from app.services.profile_loader import UserProfile


def score_job(job: NormalizedJob, user_profile: UserProfile, settings: Settings) -> float:
    cap_score = _capability_overlap(job.job_capabilities, user_profile.capabilities)
    skill_score = _skill_overlap(job.tech_stack + job.skills, user_profile.skills)
    loc_score = _location_alignment(job.location, job.remote_type, user_profile.preferences)
    comp_score = _compensation_alignment(job.salary_min, job.salary_max, user_profile.constraints)

    return (
        settings.score_capability_weight * cap_score
        + settings.score_skill_weight * skill_score
        + settings.score_location_weight * loc_score
        + settings.score_compensation_weight * comp_score
    )


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
) -> float:
    preferred_locations = preferences.get("preferred_locations") or []
    acceptable_locations = preferences.get("acceptable_locations") or []

    if remote_type == "remote":
        if "Remote" in preferred_locations:
            return 1.0
        return 0.7

    for loc in preferred_locations:
        if isinstance(loc, str) and loc.lower() in (job_location or "").lower():
            return 1.0
    for loc in acceptable_locations:
        if isinstance(loc, str) and loc.lower() in (job_location or "").lower():
            return 0.5
    return 0.0


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
