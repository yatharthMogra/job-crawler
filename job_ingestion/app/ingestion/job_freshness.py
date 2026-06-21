from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from enum import StrEnum
from typing import Any, Optional

from app.config import Settings, get_settings
from app.ingestion.extractor.deterministic import (
    extract_deterministic_fields,
    resolve_workday_posted_at,
)


class FreshnessVerdict(StrEnum):
    FRESH = "fresh"
    STALE = "stale"
    UNKNOWN = "unknown"


def _coerce_reference(reference: datetime | None) -> datetime:
    if reference is None:
        return datetime.now(timezone.utc)
    if reference.tzinfo is None:
        return reference.replace(tzinfo=timezone.utc)
    return reference


def _normalize_posted_at(posted_at: datetime) -> datetime:
    if posted_at.tzinfo is None:
        return posted_at.replace(tzinfo=timezone.utc)
    return posted_at


def classify_posted_at(
    posted_at: datetime | None,
    *,
    reference: datetime | None = None,
    max_age_days: int | None = None,
    settings: Settings | None = None,
) -> FreshnessVerdict:
    if posted_at is None:
        return FreshnessVerdict.UNKNOWN
    ref = _coerce_reference(reference)
    if max_age_days is None:
        max_age_days = (settings or get_settings()).job_max_age_days
    posted = _normalize_posted_at(posted_at)
    age = ref - posted
    if age > timedelta(days=max_age_days):
        return FreshnessVerdict.STALE
    return FreshnessVerdict.FRESH


def resolve_posted_at(
    job: dict[str, Any],
    platform: str,
    *,
    reference: datetime | None = None,
) -> datetime | None:
    ref = _coerce_reference(reference)
    platform_key = platform.lower()
    if platform_key == "workday":
        return resolve_workday_posted_at(job, reference=ref.date())
    fields = extract_deterministic_fields(job, platform=platform_key)
    return fields.get("posted_at")


def classify_job(
    job: dict[str, Any],
    platform: str,
    *,
    reference: datetime | None = None,
    max_age_days: int | None = None,
    settings: Settings | None = None,
) -> FreshnessVerdict:
    max_days = max_age_days
    if max_days is None:
        max_days = (settings or get_settings()).job_max_age_days
    posted_at = resolve_posted_at(job, platform, reference=reference)
    return classify_posted_at(posted_at, reference=reference, max_age_days=max_days)


def is_stale(
    posted_at: datetime | None,
    *,
    reference: datetime | None = None,
    max_age_days: int | None = None,
) -> bool:
    return classify_posted_at(posted_at, reference=reference, max_age_days=max_age_days) == FreshnessVerdict.STALE


def filter_fetched_jobs(
    jobs: list[dict[str, Any]],
    platform: str,
    *,
    reference: datetime | None = None,
    max_age_days: int | None = None,
) -> tuple[list[dict[str, Any]], int]:
    kept: list[dict[str, Any]] = []
    rejected = 0
    for job in jobs:
        if classify_job(job, platform, reference=reference, max_age_days=max_age_days) == FreshnessVerdict.STALE:
            rejected += 1
        else:
            kept.append(job)
    return kept, rejected


def refresh_posted_at_verdict(
    posted_at: datetime | None,
    raw_payload: object,
    platform: str,
    *,
    settings: Settings | None = None,
) -> tuple[datetime | None, FreshnessVerdict]:
    resolved = posted_at
    if isinstance(raw_payload, dict):
        extracted = resolve_posted_at(raw_payload, platform)
        if extracted is not None:
            resolved = extracted
    return resolved, classify_posted_at(resolved, settings=settings)


_RELATIVE_POSTED_DAYS = re.compile(r"posted\s+(\d+)\s+days?\s+ago", re.IGNORECASE)
_RELATIVE_POSTED_DAYS_PLUS = re.compile(r"posted\s+(\d+)\+\s+days?\s+ago", re.IGNORECASE)


def _parse_workday_absolute_date(value: str) -> date | None:
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def workday_listing_recency_hint(
    posted_on: object,
    reference_date: datetime,
    max_age_days: int,
) -> Optional[bool]:
    """Return True if listing looks fresh, False if stale, None if unknown."""
    if not posted_on or not isinstance(posted_on, str):
        return None
    reference = reference_date.date()
    lowered = posted_on.strip().lower()
    plus_match = _RELATIVE_POSTED_DAYS_PLUS.search(posted_on)
    if plus_match:
        minimum_days = int(plus_match.group(1))
        if minimum_days >= max_age_days:
            return False
        return None
    if "today" in lowered or "yesterday" in lowered:
        return True
    match = _RELATIVE_POSTED_DAYS.search(posted_on)
    if match:
        return int(match.group(1)) <= max_age_days
    parsed = _parse_workday_absolute_date(posted_on)
    if parsed is not None:
        return (reference - parsed) <= timedelta(days=max_age_days)
    return None
