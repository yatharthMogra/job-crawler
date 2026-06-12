from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.scoring.location import location_alignment_score, locations_match
from app.scoring.recommendation import score_job


def test_locations_match_ny_variants() -> None:
    assert locations_match("NY, USA", "New York, NY, United States")
    assert locations_match("New York, USA", "New York, NY")


def test_locations_match_multi_segment_job() -> None:
    assert locations_match("NY, USA", "San Francisco, CA • New York, NY • United States")


def test_location_alignment_neutral_without_prefs() -> None:
    score, _ = location_alignment_score("Berlin, Germany", "onsite", {}, constraints={})
    assert score == 0.5


def test_extract_job_country_maharashtra_not_massachusetts() -> None:
    from app.scoring.country import extract_job_country

    assert extract_job_country("Pune City, Maharashtra, India") == "IN"


def test_location_alignment_us_default_penalizes_india() -> None:
    score, _ = location_alignment_score(
        "Gurugram, HR, India",
        "onsite",
        {},
        job_country="IN",
        constraints={"work_authorization": "CPT_OPT"},
    )
    assert score == 0.15


def test_location_alignment_us_default_penalizes_germany() -> None:
    score, _ = location_alignment_score(
        "Berlin, Germany",
        "onsite",
        {},
        job_country="DE",
        constraints={"work_authorization": "CPT_OPT"},
    )
    assert score == 0.15


def test_location_alignment_explicit_us_and_ny() -> None:
    prefs = {
        "preferred_countries": ["US"],
        "preferred_states": ["NY"],
        "preferred_cities": ["New York"],
    }
    score, _ = location_alignment_score(
        "New York, NY, USA",
        "onsite",
        prefs,
        job_country="US",
        constraints={},
    )
    assert score == 1.0


def test_location_alignment_us_country_state_miss() -> None:
    prefs = {"preferred_countries": ["US"], "preferred_states": ["NY"]}
    score, _ = location_alignment_score(
        "Sunrise, FL, United States",
        "onsite",
        prefs,
        job_country="US",
        constraints={},
    )
    assert score == 0.55


def test_location_alignment_remote_with_preference() -> None:
    score, matched = location_alignment_score(
        "Remote - US",
        "remote",
        {"remote_preference": "Remote"},
        constraints={"work_authorization": "CPT_OPT"},
    )
    assert score == 1.0
    assert matched is None


def test_score_job_location_boost_us_candidate() -> None:
    job = SimpleNamespace(
        title="Data Scientist",
        job_capabilities=["Machine Learning"],
        tech_stack=["Python"],
        skills=[],
        location="New York, NY",
        job_country="US",
        remote_type="onsite",
        salary_min=100000,
        salary_max=150000,
        seniority="MID",
    )
    profile = SimpleNamespace(
        capabilities=[SimpleNamespace(capability_name="Machine Learning")],
        skills={"skills": ["Python"]},
        preferences={"preferred_countries": ["US"], "preferred_states": ["NY"]},
        constraints={},
    )
    from app.config import get_settings

    settings = get_settings()
    assert score_job(job, profile, settings) > 0.4


def test_legacy_preferred_locations_fallback() -> None:
    score, matched = location_alignment_score(
        "New York, NY",
        "onsite",
        {"preferred_locations": ["NY, USA", "New York, USA"]},
        constraints={},
    )
    assert score == 1.0
    assert matched is not None
