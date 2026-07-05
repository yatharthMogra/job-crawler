"""Tests for resolve_reference_at."""

from __future__ import annotations

from datetime import datetime, timezone

from app.ingestion.job_timestamp import resolve_reference_at


def test_resolve_reference_at_uses_source_posted_at() -> None:
    posted = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)
    fetch = datetime(2026, 6, 10, 8, 0, tzinfo=timezone.utc)
    assert resolve_reference_at(posted, fetch) == posted


def test_resolve_reference_at_falls_back_to_fetch_timestamp() -> None:
    fetch = datetime(2026, 6, 10, 8, 0, tzinfo=timezone.utc)
    assert resolve_reference_at(None, fetch) == fetch


def test_resolve_reference_at_normalizes_naive_to_utc() -> None:
    posted = datetime(2026, 6, 1, 12, 0)
    fetch = datetime(2026, 6, 10, 8, 0, tzinfo=timezone.utc)
    resolved = resolve_reference_at(posted, fetch)
    assert resolved.tzinfo == timezone.utc
    assert resolved == posted.replace(tzinfo=timezone.utc)
