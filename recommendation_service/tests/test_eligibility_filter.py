from __future__ import annotations

from unittest.mock import MagicMock

from app.config import Settings
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile


def _profile(**kwargs) -> UserProfile:
    return UserProfile(
        candidate_id=MagicMock(),
        email="a@b.com",
        name="Test",
        constraints=kwargs.get("constraints", {}),
        preferences=kwargs.get("preferences", {}),
        skills={},
    )


def test_eligibility_exclusion_adds_clearance_and_sponsorship_filters() -> None:
    profile = _profile(constraints={"sponsorship_required": True})
    settings = Settings(
        role_intent_filter_enabled=False,
        clearance_filter_enabled=False,
        domain_filter_enabled=False,
        experience_tier_visibility_enabled=False,
    )
    with_flag = build_constraint_filters(profile, settings)
    without_flag = build_constraint_filters(
        _profile(constraints={"sponsorship_required": False}),
        settings,
    )
    assert len(with_flag) == len(without_flag) + 2
