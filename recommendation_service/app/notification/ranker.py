from __future__ import annotations

import re
from datetime import timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.recommendation import score_job
from app.services.h1b_lookup import H1bLookup
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


def select_top_jobs(
    ranked: list[tuple[NormalizedJob, float]],
    limit: int,
    *,
    max_per_company: int = 1,
) -> list[tuple[NormalizedJob, float]]:
    """Pick top jobs with at most max_per_company entries per company."""
    if max_per_company <= 0:
        return ranked[:limit]

    selected: list[tuple[NormalizedJob, float]] = []
    counts: dict[str, int] = {}
    for job, score in ranked:
        company = job.company_name.lower().strip()
        if counts.get(company, 0) >= max_per_company:
            continue
        selected.append((job, score))
        counts[company] = counts.get(company, 0) + 1
        if len(selected) >= limit:
            break
    return selected


def _rank_sort_key(item: tuple[NormalizedJob, float]) -> tuple[float, float, float]:
    job, score = item
    posted_at = job.posted_at
    if posted_at is not None:
        if posted_at.tzinfo is None:
            posted_at = posted_at.replace(tzinfo=timezone.utc)
        posted_ts = posted_at.timestamp()
    else:
        posted_ts = 0.0
    return (score, job.opportunity_score or 0.0, posted_ts)


def rank_jobs(
    jobs: list[NormalizedJob],
    user_profile: UserProfile,
    settings: Settings,
    *,
    h1b_lookup: H1bLookup | None = None,
) -> list[tuple[NormalizedJob, float]]:
    scored = [(job, score_job(job, user_profile, settings, h1b_lookup=h1b_lookup)) for job in jobs]
    scored.sort(key=_rank_sort_key, reverse=True)
    return scored


async def rank_jobs_with_h1b(
    db: AsyncSession,
    jobs: list[NormalizedJob],
    user_profile: UserProfile,
    settings: Settings,
) -> list[tuple[NormalizedJob, float]]:
    # H-1B company history is not used for ranking; eligibility uses explicit job flags in retrieval.
    return rank_jobs(jobs, user_profile, settings, h1b_lookup=None)
