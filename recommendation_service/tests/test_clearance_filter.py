from __future__ import annotations

from unittest.mock import MagicMock

from app.config import Settings
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile


def test_clearance_filter_disabled_by_default() -> None:
    profile = UserProfile(
        candidate_id=MagicMock(),
        email="a@b.com",
        name="Test",
        constraints={"has_clearance": False},
        preferences={},
        skills={},
    )
    with_clearance = build_constraint_filters(
        profile,
        Settings(clearance_filter_enabled=True),
    )
    without_clearance = build_constraint_filters(
        profile,
        Settings(clearance_filter_enabled=False),
    )
    assert len(with_clearance) == len(without_clearance) + 1


def test_clearance_filter_excludes_requires_clearance_jobs() -> None:
    profile = UserProfile(
        candidate_id=MagicMock(),
        email="a@b.com",
        name="Test",
        constraints={"has_clearance": False},
        preferences={},
        skills={},
    )
    filters = build_constraint_filters(profile, Settings(clearance_filter_enabled=True))
    assert len(filters) >= 1
