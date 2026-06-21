from datetime import datetime, timedelta, timezone

import pytest

from app.ingestion.extractor.deterministic import (
    _parse_workday_date,
    extract_deterministic_fields,
    resolve_workday_posted_at,
)
from app.ingestion.job_freshness import (
    FreshnessVerdict,
    classify_job,
    classify_posted_at,
    filter_fetched_jobs,
    is_stale,
    workday_listing_recency_hint,
)


def test_classify_posted_at_fresh() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    posted = reference - timedelta(days=3)
    assert classify_posted_at(posted, reference=reference, max_age_days=7) == FreshnessVerdict.FRESH


def test_classify_posted_at_stale() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    posted = reference - timedelta(days=10)
    assert classify_posted_at(posted, reference=reference, max_age_days=7) == FreshnessVerdict.STALE


def test_classify_posted_at_unknown() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    assert classify_posted_at(None, reference=reference, max_age_days=7) == FreshnessVerdict.UNKNOWN


def test_is_stale_wrapper() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    assert is_stale(reference - timedelta(days=30), reference=reference, max_age_days=7) is True


def test_parse_workday_relative_date() -> None:
    reference = datetime(2026, 6, 19).date()
    parsed = _parse_workday_date("Posted 5 Days Ago", reference=reference)
    assert parsed is not None
    assert parsed.date() == datetime(2026, 6, 14).date()


def test_parse_workday_relative_plus_date() -> None:
    reference = datetime(2026, 6, 19).date()
    parsed = _parse_workday_date("Posted 30+ Days Ago", reference=reference)
    assert parsed is not None
    assert parsed.date() == datetime(2026, 5, 20).date()


def test_resolve_workday_posted_at_from_job() -> None:
    reference = datetime(2026, 6, 19).date()
    job = {"postedOn": "Posted 3 Days Ago", "jobPostingInfo": {}}
    parsed = resolve_workday_posted_at(job, reference=reference)
    assert parsed is not None
    assert classify_posted_at(
        parsed,
        reference=datetime(2026, 6, 19, tzinfo=timezone.utc),
        max_age_days=7,
    ) == FreshnessVerdict.FRESH


def test_classify_workday_job_stale() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    job = {"postedOn": "Posted 30 Days Ago", "jobPostingInfo": {}}
    assert classify_job(job, "workday", reference=reference, max_age_days=7) == FreshnessVerdict.STALE


def test_classify_lever_job_stale() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    created_ms = int((reference - timedelta(days=30)).timestamp() * 1000)
    job = {"id": "abc", "text": "Engineer", "createdAt": created_ms, "categories": {}}
    assert classify_job(job, "lever", reference=reference, max_age_days=7) == FreshnessVerdict.STALE


def test_classify_greenhouse_unknown_without_post_date() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    job = {
        "id": 1,
        "title": "Engineer",
        "updated_at": reference.isoformat(),
        "location": {"name": "Remote"},
        "departments": [],
        "absolute_url": "https://example.com/jobs/1",
    }
    assert classify_job(job, "greenhouse", reference=reference, max_age_days=7) == FreshnessVerdict.UNKNOWN


def test_classify_greenhouse_fresh_with_created_at() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    job = {
        "id": 1,
        "title": "Engineer",
        "created_at": (reference - timedelta(days=2)).isoformat().replace("+00:00", "Z"),
        "location": {"name": "Remote"},
        "departments": [],
        "absolute_url": "https://example.com/jobs/1",
    }
    assert classify_job(job, "greenhouse", reference=reference, max_age_days=7) == FreshnessVerdict.FRESH


def test_filter_fetched_jobs() -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    fresh_ms = int((reference - timedelta(days=1)).timestamp() * 1000)
    stale_ms = int((reference - timedelta(days=20)).timestamp() * 1000)
    jobs = [
        {"id": "1", "text": "Fresh", "createdAt": fresh_ms, "categories": {}},
        {"id": "2", "text": "Stale", "createdAt": stale_ms, "categories": {}},
    ]
    kept, rejected = filter_fetched_jobs(jobs, "lever", reference=reference, max_age_days=7)
    assert rejected == 1
    assert len(kept) == 1
    assert kept[0]["id"] == "1"


@pytest.mark.parametrize(
    ("posted_on", "expected"),
    [
        ("Posted 5 Days Ago", True),
        ("Posted 30+ Days Ago", False),
        ("not-a-date", None),
    ],
)
def test_workday_listing_recency_hint(posted_on: str, expected: bool | None) -> None:
    reference = datetime(2026, 6, 19, tzinfo=timezone.utc)
    assert workday_listing_recency_hint(posted_on, reference, 7) is expected
