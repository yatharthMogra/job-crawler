from __future__ import annotations

import uuid

from datetime import datetime, timezone

from app.notification.company_watch_watermark import job_reference_at_after_watermark
from app.notification.filters import build_digest_filters, job_matches_location_constraints
from app.services.profile_loader import UserProfile


class _JobStub:
    def __init__(self, *, location: str | None, remote_type: str) -> None:
        self.location = location
        self.remote_type = remote_type


def test_build_digest_filters_employment_type() -> None:
    filters = build_digest_filters({"employment_type": "internship"})
    assert len(filters) == 1


def test_build_digest_filters_empty() -> None:
    assert build_digest_filters(None) == []
    assert build_digest_filters({}) == []


def test_job_matches_location_constraints_no_prefs() -> None:
    job = _JobStub(location="New York, NY", remote_type="onsite")
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="a@b.com",
        name="Test",
        constraints={},
        preferences={},
        skills={},
    )
    assert job_matches_location_constraints(job, profile) is True


def test_job_matches_location_constraints_preferred() -> None:
    job = _JobStub(location="San Francisco, CA", remote_type="onsite")
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="a@b.com",
        name="Test",
        constraints={},
        preferences={"preferred_locations": ["San Francisco, CA"]},
        skills={},
    )
    assert job_matches_location_constraints(job, profile) is True


def test_job_matches_location_constraints_mismatch() -> None:
    job = _JobStub(location="Austin, TX", remote_type="onsite")
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="a@b.com",
        name="Test",
        constraints={},
        preferences={"preferred_locations": ["New York, NY"]},
        skills={},
    )
    assert job_matches_location_constraints(job, profile) is False


class _JobRefStub:
    def __init__(self, reference_at: datetime | None) -> None:
        self.reference_at = reference_at


def test_job_reference_at_after_watermark_strictly_greater() -> None:
    watermark = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
    assert job_reference_at_after_watermark(
        _JobRefStub(datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)),
        watermark,
    ) is False
    assert job_reference_at_after_watermark(
        _JobRefStub(datetime(2026, 7, 1, 12, 1, tzinfo=timezone.utc)),
        watermark,
    ) is True
    assert job_reference_at_after_watermark(_JobRefStub(None), watermark) is False
    assert job_reference_at_after_watermark(_JobRefStub(datetime(2026, 7, 2, tzinfo=timezone.utc)), None) is False
