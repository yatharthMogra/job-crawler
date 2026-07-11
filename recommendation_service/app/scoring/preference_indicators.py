from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.models.shared import NormalizedJob
from app.scoring.location import location_alignment_score
from app.services.profile_loader import UserProfile


@dataclass(frozen=True)
class PreferenceIndicator:
    label: str
    kind: Literal["strength", "gap"]


def preference_indicators(
    job: NormalizedJob,
    profile: UserProfile,
) -> list[PreferenceIndicator]:
    preferences = profile.preferences or {}
    constraints = profile.constraints or {}
    indicators: list[PreferenceIndicator] = []

    location_score, _ = location_alignment_score(
        job.location,
        job.remote_type,
        preferences,
        job_country=job.job_country,
        constraints=constraints,
    )
    remote_preference = str(preferences.get("remote_preference") or "").lower().strip()
    accepts_remote = remote_preference in {
        "",
        "remote",
        "hybrid",
        "hybrid_or_remote",
        "no_preference",
        "any",
    }
    if job.remote_type == "remote" and accepts_remote:
        indicators.append(PreferenceIndicator("Remote-friendly", "strength"))
    elif location_score >= 0.9:
        indicators.append(PreferenceIndicator("Matches your location", "strength"))
    elif location_score <= 0.3:
        indicators.append(PreferenceIndicator("Outside preferred location", "gap"))

    minimum_salary = constraints.get("minimum_salary")
    minimum_hourly_rate = constraints.get("minimum_hourly_rate")
    if minimum_salary or minimum_hourly_rate:
        if minimum_salary and job.salary_max is not None:
            if job.salary_max >= minimum_salary:
                indicators.append(PreferenceIndicator("Meets salary expectations", "strength"))
            else:
                indicators.append(PreferenceIndicator("Below your salary minimum", "gap"))

    return indicators
