from __future__ import annotations

from unittest.mock import MagicMock

from app.config import Settings
from app.domain import build_domain_filters, candidate_domains_from_profile
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile


def test_candidate_domains_from_profile() -> None:
    assert candidate_domains_from_profile("Software", None) == ["Software"]
    assert candidate_domains_from_profile("Software", "Data_Analytics") == [
        "Software",
        "Data_Analytics",
    ]
    assert candidate_domains_from_profile("Other", None) == []


def test_build_constraint_filters_includes_domain_when_enabled() -> None:
    profile = UserProfile(
        candidate_id=MagicMock(),
        email="a@b.com",
        name="Test",
        constraints={},
        preferences={},
        skills={},
        primary_domain="Software",
    )
    settings = Settings(domain_filter_enabled=True)
    with_domain = build_constraint_filters(profile, settings)
    without_domain = build_constraint_filters(
        profile,
        Settings(domain_filter_enabled=False),
    )
    assert len(with_domain) == len(without_domain) + 1


def test_build_domain_filters_empty_without_domains() -> None:
    assert build_domain_filters([]) == []
