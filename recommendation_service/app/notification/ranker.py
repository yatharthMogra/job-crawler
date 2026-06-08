from __future__ import annotations

import re

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.recommendation import score_job
from app.services.profile_loader import UserProfile

_WHITESPACE = re.compile(r"\s+")


def normalize_title(title: str) -> str:
    normalized = title.lower().strip()
    normalized = _WHITESPACE.sub(" ", normalized)
    return normalized.rstrip(".,;:")


def deduplicate_ranked_jobs(
    ranked: list[tuple[NormalizedJob, float]],
) -> list[tuple[NormalizedJob, float]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[tuple[NormalizedJob, float]] = []
    for job, score in ranked:
        key = (job.company_name.lower().strip(), normalize_title(job.title))
        if key in seen:
            continue
        seen.add(key)
        deduped.append((job, score))
    return deduped


def rank_jobs(
    jobs: list[NormalizedJob],
    user_profile: UserProfile,
    settings: Settings,
) -> list[tuple[NormalizedJob, float]]:
    scored = [(job, score_job(job, user_profile, settings)) for job in jobs]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored
