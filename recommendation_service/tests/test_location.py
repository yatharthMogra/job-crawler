from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.location import (
    _normalize_text,
    location_alignment_score,
    location_tokens,
    locations_match,
)
from app.scoring.recommendation import score_job
from app.services.profile_loader import UserProfile


def test_locations_match_ny_usa_to_new_york_ny() -> None:
    assert locations_match("NY, USA", "New York, NY")


def test_locations_match_new_york_usa_to_new_york_ny() -> None:
    assert locations_match("New York, USA", "New York, NY")


def test_locations_match_multi_segment_job() -> None:
    job_location = "San Francisco, CA; New York, NY; Remote"
    assert locations_match("NY, USA", job_location)
    assert not locations_match("Chicago, IL", job_location)


def test_parenthetical_hq_strips_before_normalization() -> None:
    assert _normalize_text("ny (hq)") == "ny"
    assert _normalize_text("New York, NY (HQ)") == "new york, ny"
    assert "new_york" in location_tokens("NY (HQ)")


def test_locations_match_ramp_hq_and_slash_separated() -> None:
    assert locations_match("NY, USA", "New York, NY (HQ)")
    assert locations_match("NY, USA", "New York, NY (HQ) / San Francisco, CA")


def test_location_alignment_score_multi_segment_sf_ny_is_full_credit() -> None:
    ny_prefs = {"preferred_locations": ["NY, USA", "New York, USA"], "acceptable_locations": []}
    for job_location in (
        "San Francisco, CA; New York, NY",
        "San Francisco, CA • New York, NY • United States",
        "New York, NY (HQ)",
    ):
        score, matched = location_alignment_score(job_location, "unclear", ny_prefs)
        assert score == 1.0
        assert matched == "NY, USA"


def test_locations_match_non_match() -> None:
    assert not locations_match("NY, USA", "London, UK")
    assert not locations_match("NY, USA", None)


def test_location_alignment_score_preferred_match() -> None:
    score, matched = location_alignment_score(
        "New York, NY",
        "hybrid",
        {"preferred_locations": ["NY, USA"], "acceptable_locations": []},
    )
    assert score == 1.0
    assert matched == "NY, USA"


def test_location_alignment_score_acceptable_match() -> None:
    score, matched = location_alignment_score(
        "London, UK",
        "onsite",
        {"preferred_locations": ["NY, USA"], "acceptable_locations": ["London, UK"]},
    )
    assert score == 0.5
    assert matched == "London, UK"


def test_score_job_ny_preference_boosts_ny_job() -> None:
    settings = Settings()
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        constraints={},
        preferences={"preferred_locations": ["NY, USA", "New York, USA"]},
        skills={"languages": ["Python"], "frameworks": [], "tools": [], "databases": [], "other": []},
        capabilities=[SimpleNamespace(capability_name="Backend Engineering")],
    )
    base_kwargs = {
        "title": "Backend Engineer",
        "company_name": "Acme",
        "posting_url": "https://example.com",
        "posted_at": None,
        "is_active": True,
        "processing_state": "success",
        "seniority": "junior",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "yes",
        "sponsorship_confidence": "high",
        "remote_type": "hybrid",
        "tech_stack": ["Python"],
        "skills": [],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "LOW",
        "retrieval_pools": ["BACKEND_ENGINEER_FULLTIME"],
        "salary_min": 120_000,
        "salary_max": 150_000,
        "opportunity_score": 0.8,
        "created_at": datetime.now(timezone.utc),
    }
    ny_job = NormalizedJob(id=uuid.uuid4(), location="New York, NY", **base_kwargs)
    london_job = NormalizedJob(id=uuid.uuid4(), location="London, UK", **base_kwargs)

    ny_score = score_job(ny_job, profile, settings)
    london_score = score_job(london_job, profile, settings)
    assert ny_score > london_score
