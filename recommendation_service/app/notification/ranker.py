from __future__ import annotations

import math
import re
from datetime import timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.recommendation import score_job
from app.services.h1b_lookup import H1bLookup, load_h1b_summary_lookup
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


def select_diversified_jobs(
    ranked: list[tuple[NormalizedJob, float]],
    limit: int,
    *,
    applied_count_by_company: dict[str, int],
    max_share: float,
    unlock_batch_size: int,
) -> list[tuple[NormalizedJob, float]]:
    """Pick top jobs with per-company share cap and apply-based batch unlock."""
    if limit <= 0:
        return []
    if max_share <= 0:
        return ranked[:limit]

    base_cap = max(1, math.ceil(limit * max_share))
    batch = max(1, unlock_batch_size)
    selected: list[tuple[NormalizedJob, float]] = []
    visible_counts: dict[str, int] = {}

    for job, score in ranked:
        company = job.company_name.lower().strip()
        applied = applied_count_by_company.get(company, 0)
        allowed = base_cap + (applied // batch) * batch
        if visible_counts.get(company, 0) >= allowed:
            continue
        selected.append((job, score))
        visible_counts[company] = visible_counts.get(company, 0) + 1
        if len(selected) >= limit:
            break
    return selected


def _reference_timestamp(job: NormalizedJob) -> float:
    ts = job.reference_at or job.posted_at
    if ts is None:
        ts = job.created_at
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.timestamp()


def _rank_sort_key(item: tuple[NormalizedJob, float]) -> tuple[float, float, float]:
    job, score = item
    return (score, job.opportunity_score or 0.0, _reference_timestamp(job))


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
    h1b_lookup: H1bLookup | None = None
    constraints = user_profile.constraints or {}
    if settings.sponsorship_score_enabled and constraints.get("sponsorship_required"):
        company_ids = {job.company_id for job in jobs}
        h1b_lookup = await load_h1b_summary_lookup(db, company_ids)
    return rank_jobs(jobs, user_profile, settings, h1b_lookup=h1b_lookup)
