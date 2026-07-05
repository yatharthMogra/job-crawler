from __future__ import annotations

from datetime import datetime, timezone


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def resolve_reference_at(
    source_posted_at: datetime | None,
    fetch_timestamp: datetime,
) -> datetime:
    """Canonical job timestamp: source posted_at when present, else fetch_timestamp."""
    if source_posted_at is not None:
        return _ensure_utc(source_posted_at)
    return _ensure_utc(fetch_timestamp)
