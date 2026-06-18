from __future__ import annotations

import re
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.normalized_job import NormalizedJob

_ARTICLE_PATTERN = re.compile(r"\b(the|a|an|inc|llc|corp|ltd)\b")
_PUNCT_PATTERN = re.compile(r"[^a-z0-9 ]")
_SPACE_PATTERN = re.compile(r"\s+")


def _normalize_fingerprint_part(value: str) -> str:
    s = value.lower().strip()
    s = _PUNCT_PATTERN.sub(" ", s)
    s = _ARTICLE_PATTERN.sub("", s)
    return _SPACE_PATTERN.sub(" ", s).strip()


def build_dedup_fingerprint(company: str, title: str, location: str | None) -> str:
    """Normalized fingerprint for cross-platform job deduplication."""
    co = _normalize_fingerprint_part(company)[:40]
    title_words = _normalize_fingerprint_part(title).split()[:4]
    loc_part = (location or "").split(",")[0]
    loc = _normalize_fingerprint_part(loc_part)[:20]
    return f"{co}|{' '.join(title_words)}|{loc}"


async def fingerprint_exists(
    db: AsyncSession,
    fingerprint: str,
    *,
    company_id: UUID,
    external_job_id: str,
) -> bool:
    """Return True if another active job already has this fingerprint."""
    stmt = (
        select(NormalizedJob.id)
        .where(NormalizedJob.dedup_fingerprint == fingerprint)
        .where(NormalizedJob.is_active.is_(True))
        .where(
            or_(
                NormalizedJob.company_id != company_id,
                NormalizedJob.external_job_id != external_job_id,
            )
        )
        .limit(1)
    )
    result = await db.scalar(stmt)
    return result is not None
