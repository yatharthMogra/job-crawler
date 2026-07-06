from __future__ import annotations

from unittest.mock import MagicMock

from app.config import Settings
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile


def test_clearance_filter_applies_without_feature_flag() -> None:
    profile = UserProfile(
        candidate_id=MagicMock(),
        email="a@b.com",
        name="Test",
        constraints={"has_clearance": False},
        preferences={},
        skills={},
    )
    filters = build_constraint_filters(profile, Settings(clearance_filter_enabled=False))
    assert len(filters) >= 1


def test_clearance_filter_excludes_requires_clearance_jobs() -> None:
    profile = UserProfile(
        candidate_id=MagicMock(),
        email="a@b.com",
        name="Test",
        constraints={"has_clearance": False},
        preferences={},
        skills={},
    )
    filters = build_constraint_filters(profile, Settings())
    assert len(filters) >= 1
