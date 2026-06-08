from __future__ import annotations

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.recommendation import score_job
from app.services.profile_loader import UserProfile


def rank_jobs(
    jobs: list[NormalizedJob],
    user_profile: UserProfile,
    settings: Settings,
) -> list[tuple[NormalizedJob, float]]:
    scored = [(job, score_job(job, user_profile, settings)) for job in jobs]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored
