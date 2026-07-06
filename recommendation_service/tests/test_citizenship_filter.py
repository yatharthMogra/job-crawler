from __future__ import annotations

from unittest.mock import MagicMock

from app.config import Settings
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile


def _profile(**kwargs: object) -> UserProfile:
    defaults = {
        "candidate_id": MagicMock(),
        "email": "a@b.com",
        "name": "Test",
        "constraints": {},
        "preferences": {},
        "skills": {},
    }
    defaults.update(kwargs)
    return UserProfile(**defaults)


def test_clearance_filter_always_applies_when_user_lacks_clearance() -> None:
    profile = _profile(constraints={"has_clearance": False})
    filters = build_constraint_filters(profile, Settings())
    assert len(filters) >= 1


def test_clearance_filter_skipped_when_user_has_clearance() -> None:
    profile = _profile(constraints={"has_clearance": True})
    without_clearance = _profile(constraints={"has_clearance": False})
    assert len(build_constraint_filters(profile, Settings())) == len(
        build_constraint_filters(without_clearance, Settings())
    ) - 1


def test_citizenship_filter_applies_when_sponsorship_required() -> None:
    profile = _profile(constraints={"sponsorship_required": True})
    without = _profile(constraints={"sponsorship_required": False})
    assert len(build_constraint_filters(profile, Settings())) == len(
        build_constraint_filters(without, Settings())
    ) + 1


def test_sponsorship_and_clearance_filters_stack() -> None:
    profile = _profile(constraints={"sponsorship_required": True, "has_clearance": False})
    filters = build_constraint_filters(profile, Settings())
    assert len(filters) >= 2
