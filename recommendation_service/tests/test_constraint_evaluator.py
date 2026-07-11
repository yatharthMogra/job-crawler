"""Parity tests: in-process constraints vs SQL build_constraint_filters logic."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.config import Settings
from app.constraints.evaluator import RankingJob, job_passes_constraints
from app.notification.retrieval import build_constraint_filters
from app.services.profile_loader import UserProfile


def _profile(**kwargs) -> UserProfile:
    return UserProfile(
        candidate_id=uuid4(),
        email="a@b.com",
        name="Test",
        constraints=kwargs.get("constraints", {}),
        preferences=kwargs.get("preferences", {}),
        skills={},
        primary_domain=kwargs.get("primary_domain"),
        secondary_domain=kwargs.get("secondary_domain"),
    )


def _job(**overrides) -> RankingJob:
    now = datetime.now(timezone.utc)
    base = dict(
        id=uuid4(),
        company_id=uuid4(),
        title="Engineer",
        company_name="Acme",
        location="SF",
        job_country="US",
        posting_url=None,
        posted_at=now,
        reference_at=now,
        created_at=now,
        remote_type="hybrid",
        application_effort="LOW",
        salary_min=100000,
        salary_max=150000,
        opportunity_score=0.8,
        retrieval_pools=["SOFTWARE_ENGINEER_FULLTIME"],
        normalized_roles=["SOFTWARE_ENGINEER"],
        job_capabilities=[],
        tech_stack=[],
        skills=[],
        seniority="MID",
        experience_tier="MID",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="yes",
        sponsorship_confidence="high",
        requires_clearance=False,
        requires_citizenship=False,
        role_intent="IC",
        job_domain="Software",
        job_secondary_domain=None,
        content_embedding=None,
    )
    base.update(overrides)
    return RankingJob(**base)


def _settings(**kwargs) -> Settings:
    defaults = dict(
        role_intent_filter_enabled=False,
        domain_filter_enabled=False,
        experience_tier_visibility_enabled=False,
        clearance_filter_enabled=False,
    )
    defaults.update(kwargs)
    return Settings(**defaults)


def test_clearance_blocks_when_user_lacks_clearance() -> None:
    profile = _profile(constraints={"has_clearance": False})
    settings = _settings()
    assert job_passes_constraints(_job(requires_clearance=True), profile, settings) is False
    assert job_passes_constraints(_job(requires_clearance=False), profile, settings) is True


def test_sponsorship_required() -> None:
    profile = _profile(constraints={"sponsorship_required": True})
    settings = _settings()
    assert job_passes_constraints(_job(sponsorship_status="no"), profile, settings) is False
    assert job_passes_constraints(_job(sponsorship_status="yes"), profile, settings) is True
    assert job_passes_constraints(_job(sponsorship_status="unclear"), profile, settings) is True


def test_internship_only() -> None:
    profile = _profile(constraints={"internship_only": True})
    settings = _settings()
    assert job_passes_constraints(_job(is_internship=False), profile, settings) is False
    assert job_passes_constraints(_job(is_internship=True), profile, settings) is True


def test_fulltime_only() -> None:
    profile = _profile(constraints={"fulltime_only": True})
    settings = _settings()
    assert job_passes_constraints(_job(is_internship=True), profile, settings) is False
    assert job_passes_constraints(_job(is_internship=False), profile, settings) is True


def test_minimum_salary() -> None:
    profile = _profile(constraints={"minimum_salary": 120000})
    settings = _settings()
    assert job_passes_constraints(_job(salary_max=100000), profile, settings) is False
    assert job_passes_constraints(_job(salary_max=150000), profile, settings) is True
    assert job_passes_constraints(_job(salary_max=None), profile, settings) is True


def test_role_intent_filter() -> None:
    profile = _profile(preferences={"primary_role_intents": ["IC"]})
    settings = _settings(role_intent_filter_enabled=True)
    assert job_passes_constraints(_job(role_intent="IC"), profile, settings) is True
    assert job_passes_constraints(_job(role_intent="MANAGER"), profile, settings) is False
    assert job_passes_constraints(_job(role_intent=None), profile, settings) is False


def test_domain_filter() -> None:
    profile = _profile(primary_domain="Software")
    settings = _settings(domain_filter_enabled=True)
    assert job_passes_constraints(_job(job_domain="Software"), profile, settings) is True
    assert job_passes_constraints(_job(job_domain="Hardware", job_secondary_domain=None), profile, settings) is False
    assert job_passes_constraints(
        _job(job_domain="Hardware", job_secondary_domain="Software"), profile, settings
    ) is True


def test_seniority_hard_block() -> None:
    profile = _profile(constraints={"target_seniority": ["MID", "JUNIOR"]})
    settings = _settings(experience_tier_visibility_enabled=False)
    assert job_passes_constraints(_job(seniority="STAFF"), profile, settings) is False
    assert job_passes_constraints(_job(seniority="MID"), profile, settings) is True
    assert job_passes_constraints(_job(seniority="UNKNOWN"), profile, settings) is True


def test_sql_filter_count_matches_sponsorship() -> None:
    """Smoke: SQL builder still adds filters when sponsorship required."""
    profile = _profile(constraints={"sponsorship_required": True})
    settings = _settings()
    with_flag = build_constraint_filters(profile, settings)
    without = build_constraint_filters(_profile(constraints={}), settings)
    assert len(with_flag) == len(without) + 2
