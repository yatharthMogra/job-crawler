from __future__ import annotations

from unittest.mock import MagicMock

from app.config import Settings
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile
from app.services.role_intent_preferences import (
    effective_role_intents,
    pool_derived_role_intents,
    primary_role_intents,
)


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


def test_primary_role_intents_prefers_primary_field() -> None:
    prefs = {"primary_role_intents": ["engineer"], "role_intents": ["sales"]}
    assert primary_role_intents(prefs) == ["engineer"]


def test_primary_role_intents_falls_back_to_legacy() -> None:
    prefs = {"role_intents": ["analyst"]}
    assert primary_role_intents(prefs) == ["analyst"]


def test_effective_role_intents_unions_primary_and_pool() -> None:
    prefs = {
        "primary_role_intents": ["engineer"],
        "pool_role_intents": ["analyst"],
    }
    assert effective_role_intents(prefs) == ["engineer", "analyst"]


def test_effective_role_intents_deduplicates() -> None:
    prefs = {
        "primary_role_intents": ["engineer", "researcher"],
        "pool_role_intents": ["engineer", "analyst"],
    }
    assert effective_role_intents(prefs) == ["engineer", "researcher", "analyst"]


def test_pool_derived_role_intents_empty_when_unset() -> None:
    assert pool_derived_role_intents({}) == []


def test_role_intent_filter_uses_pool_derived_intents() -> None:
    profile = _profile(
        preferences={
            "primary_role_intents": ["engineer"],
            "pool_role_intents": ["analyst"],
        }
    )
    filters = build_constraint_filters(profile, Settings(role_intent_filter_enabled=True))
    assert len(filters) >= 1


def test_role_intent_filter_disabled_by_default() -> None:
    profile = _profile(preferences={"primary_role_intents": ["engineer"]})
    with_intent = build_constraint_filters(
        profile,
        Settings(role_intent_filter_enabled=True),
    )
    without_intent = build_constraint_filters(
        profile,
        Settings(role_intent_filter_enabled=False),
    )
    assert len(with_intent) == len(without_intent) + 1


def test_role_intent_filter_uses_default_when_unset() -> None:
    profile = _profile()
    filters = build_constraint_filters(profile, Settings(role_intent_filter_enabled=True))
    assert len(filters) >= 1


def test_clearance_filter_when_enabled_and_no_clearance() -> None:
    profile = _profile(constraints={"has_clearance": False})
    with_clearance = build_constraint_filters(
        profile,
        Settings(clearance_filter_enabled=True),
    )
    without_clearance = build_constraint_filters(
        profile,
        Settings(clearance_filter_enabled=False),
    )
    assert len(with_clearance) == len(without_clearance) + 1


def test_clearance_filter_skipped_when_user_has_clearance() -> None:
    profile = _profile(constraints={"has_clearance": True})
    with_flag = build_constraint_filters(
        profile,
        Settings(clearance_filter_enabled=True),
    )
    without_flag = build_constraint_filters(
        profile,
        Settings(clearance_filter_enabled=False),
    )
    assert len(with_flag) == len(without_flag)


def test_both_filters_stack() -> None:
    profile = _profile(
        constraints={"has_clearance": False},
        preferences={"primary_role_intents": ["engineer"]},
        primary_domain="Software",
    )
    all_on = build_constraint_filters(
        profile,
        Settings(
            role_intent_filter_enabled=True,
            clearance_filter_enabled=True,
            domain_filter_enabled=True,
        ),
    )
    all_off = build_constraint_filters(
        profile,
        Settings(
            role_intent_filter_enabled=False,
            clearance_filter_enabled=False,
            domain_filter_enabled=False,
        ),
    )
    assert len(all_on) == len(all_off) + 3
