from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.config import Settings
from app.models.shared import NormalizedJob
from app.notification.retrieval import build_constraint_filters
from app.scoring.experience_tier import experience_tier_distance_score, job_exceeds_visibility_ceiling
from app.scoring.recommendation import score_job
from app.services.profile_loader import UserProfile


def _job(**kwargs) -> NormalizedJob:
    defaults = {
        "id": uuid.uuid4(),
        "title": "Backend Engineer",
        "company_name": "Acme",
        "location": "New York, NY",
        "posting_url": "https://example.com",
        "posted_at": None,
        "is_active": True,
        "processing_state": "success",
        "seniority": "MID",
        "experience_tier": "MID",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "yes",
        "sponsorship_confidence": "high",
        "remote_type": "hybrid",
        "tech_stack": ["Python"],
        "skills": ["REST"],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "LOW",
        "retrieval_pools": ["BACKEND_ENGINEER_FULLTIME"],
        "salary_min": 120_000,
        "salary_max": 150_000,
        "opportunity_score": 0.8,
        "created_at": datetime.now(timezone.utc),
    }
    defaults.update(kwargs)
    return NormalizedJob(**defaults)


def _profile(**constraint_overrides) -> UserProfile:
    constraints = {
        "target_seniority": ["INTERN", "NEW_GRAD", "ENTRY", "MID"],
        "current_experience_tier": "MID",
        **constraint_overrides,
    }
    return UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        constraints=constraints,
        preferences={},
        skills={"languages": ["Python"], "frameworks": [], "tools": [], "databases": [], "other": []},
        capabilities=[],
    )


def test_experience_tier_distance_exact_match() -> None:
    assert experience_tier_distance_score("MID", "MID") == 1.0


def test_experience_tier_distance_unknown_neutral() -> None:
    assert experience_tier_distance_score("UNKNOWN", "MID") == 0.5
    assert experience_tier_distance_score("MID", "UNKNOWN") == 0.5


def test_job_exceeds_visibility_ceiling() -> None:
    assert job_exceeds_visibility_ceiling("ABOVE_SENIOR", "SENIOR") is True
    assert job_exceeds_visibility_ceiling("SENIOR", "SENIOR") is False
    assert job_exceeds_visibility_ceiling("UNKNOWN", "SENIOR") is False


def test_build_constraint_filters_uses_tier_gate_when_enabled() -> None:
    settings = Settings(experience_tier_visibility_enabled=True, experience_tier_visibility_ceiling="SENIOR")
    filters = build_constraint_filters(_profile(), settings)
    assert len(filters) >= 1


def test_score_job_tier_ranking_when_enabled() -> None:
    settings = Settings(experience_tier_score_enabled=True)
    profile = _profile()
    mid_score = score_job(_job(experience_tier="MID"), profile, settings)
    senior_score = score_job(_job(experience_tier="SENIOR", title="Senior Engineer"), profile, settings)
    assert mid_score > senior_score


def test_score_job_skips_seniority_multiplier_when_tier_enabled() -> None:
    settings = Settings(experience_tier_score_enabled=True)
    profile = _profile(current_experience_tier="MID")
    score_with_senior_label = score_job(
        _job(experience_tier="MID", seniority="SENIOR"),
        profile,
        settings,
    )
    score_with_mid_label = score_job(
        _job(experience_tier="MID", seniority="MID"),
        profile,
        settings,
    )
    assert score_with_senior_label == score_with_mid_label
