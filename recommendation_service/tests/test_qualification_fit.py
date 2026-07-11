from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from app.config import Settings
from app.models.shared import CandidateEvidence, NormalizedJob
from app.scoring.coverage import (
    best_fuzzy_match,
    capability_coverage,
    skill_coverage,
    skill_coverage_components,
)
from app.scoring.qualification_fit import (
    calibrate_qualification_fit_display,
    compute_qualification_fit,
)
from app.scoring.structural import (
    experience_adequacy_score,
    infer_candidate_experience_years,
    infer_required_experience_years,
    qualification_structural_score,
)
from app.services.profile_loader import UserProfile


def _settings(**overrides) -> Settings:
    return Settings(**overrides)


def _job(**kwargs) -> NormalizedJob:
    defaults = {
        "id": uuid.uuid4(),
        "external_job_id": "ext-1",
        "company_id": uuid.uuid4(),
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
        "tech_stack": ["Python", "AWS"],
        "skills": ["REST"],
        "required_skills": ["Python", "AWS"],
        "preferred_skills": ["Kubernetes"],
        "normalized_roles": ["BACKEND_ENGINEER"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "LOW",
        "retrieval_pools": ["BACKEND_ENGINEER_FULLTIME"],
        "salary_min": 120_000,
        "salary_max": 150_000,
        "opportunity_score": 0.8,
        "created_at": datetime.now(timezone.utc),
        "required_qualifications": ["5+ years of backend experience", "BS in Computer Science"],
        "preferred_qualifications": [],
        "responsibilities": [],
        "benefits": [],
    }
    defaults.update(kwargs)
    return NormalizedJob(**defaults)


def _profile(**kwargs) -> UserProfile:
    defaults = {
        "candidate_id": uuid.uuid4(),
        "email": "test@example.com",
        "name": "Test",
        "constraints": {"full_time_experience_years": 6.0},
        "preferences": {},
        "skills": {
            "languages": ["Python"],
            "frameworks": [],
            "tools": ["AWS"],
            "databases": [],
            "other": [],
        },
        "education": {"entries": [{"degree": "BS Computer Science"}]},
        "capabilities": [SimpleNamespace(capability_name="Backend Engineering")],
        "evidence": [],
    }
    defaults.update(kwargs)
    return UserProfile(**defaults)


def test_best_fuzzy_match_exact() -> None:
    settings = _settings()
    score = best_fuzzy_match("Python", ["Java", "Python"], settings=settings)
    assert score == 1.0


def test_best_fuzzy_match_bm25_partial_without_embeddings() -> None:
    settings = _settings()
    score = best_fuzzy_match("TypeScript", ["JavaScript"], settings=settings)
    assert 0.0 < score < 1.0


def test_best_fuzzy_match_uses_optional_embeddings() -> None:
    settings = _settings(coverage_fuzzy_bm25_weight=0.0, coverage_fuzzy_semantic_weight=1.0)
    vectors = {
        "react": [1.0, 0.0],
        "react native": [0.95, 0.05],
    }

    def embed_fn(term: str) -> list[float] | None:
        return vectors.get(term.strip().lower())

    score = best_fuzzy_match(
        "React",
        ["React Native"],
        settings=settings,
        embed_fn=embed_fn,
        embedding_min_sim=0.0,
        embedding_max_sim=1.0,
    )
    assert score > 0.8


def test_skill_coverage_prefers_required_skills() -> None:
    settings = _settings()
    profile = _profile(
        skills={
            "languages": ["Python"],
            "frameworks": [],
            "tools": [],
            "databases": [],
            "other": [],
        }
    )
    job = _job(required_skills=["Python", "Java"], preferred_skills=[])
    assert skill_coverage(job, profile, settings) == pytest.approx(0.6)


def test_skill_coverage_falls_back_to_tech_stack_when_required_empty() -> None:
    settings = _settings()
    profile = _profile(
        skills={
            "languages": ["Python"],
            "frameworks": [],
            "tools": [],
            "databases": [],
            "other": [],
        }
    )
    job = _job(required_skills=[], preferred_skills=[], tech_stack=["Python"], skills=[])
    combined, required_cov, preferred_cov = skill_coverage_components(job, profile, settings)
    assert required_cov == 1.0
    assert preferred_cov == 1.0
    assert combined == pytest.approx(1.0)


def test_capability_coverage_neutral_when_job_has_no_capabilities() -> None:
    settings = _settings()
    profile = _profile(capabilities=[])
    job = _job(job_capabilities=[])
    assert capability_coverage(job, profile, settings) == 1.0


def test_infer_required_experience_years() -> None:
    job = _job(required_qualifications=["3+ years building APIs", "BS degree"])
    assert infer_required_experience_years(job) == 3


def test_experience_adequacy_neutral_without_job_requirement() -> None:
    job = _job(required_qualifications=["BS in Computer Science"])
    profile = _profile(constraints={})
    assert experience_adequacy_score(profile, job) == 1.0


def test_experience_adequacy_linear_decay() -> None:
    job = _job(required_qualifications=["4 years experience"])
    profile = _profile(constraints={"full_time_experience_years": 2.0})
    assert experience_adequacy_score(profile, job) == pytest.approx(0.5)


def test_infer_candidate_experience_years_from_evidence_dates() -> None:
    profile = _profile(
        constraints={},
        evidence=[
            CandidateEvidence(
                id=uuid.uuid4(),
                candidate_id=uuid.uuid4(),
                evidence_type="experience",
                is_approved=True,
                is_active=True,
                raw_source_text="Built APIs",
                normalized_data={"start_date": "2020-01", "end_date": "2022-01"},
            )
        ],
    )
    assert infer_candidate_experience_years(profile) == pytest.approx(2.0, abs=0.2)


def test_qualification_structural_score_averages_experience_and_education() -> None:
    job = _job(required_qualifications=["2 years experience", "BS in Computer Science"])
    profile = _profile(
        constraints={"full_time_experience_years": 4.0},
        education={"entries": [{"degree": "BS Computer Science"}]},
    )
    structural = qualification_structural_score(profile, job)
    assert structural == pytest.approx(1.0)


def test_qualification_structural_score_is_neutral_without_requirements() -> None:
    assert qualification_structural_score(
        _profile(education={}),
        _job(required_qualifications=[]),
    ) == pytest.approx(1.0)


def test_compute_qualification_fit_raw_formula() -> None:
    settings = _settings(qualification_fit_shadow_mode=False)
    breakdown = compute_qualification_fit(_job(), _profile(), settings)
    expected = (
        settings.qualification_fit_skill_weight * breakdown.skill_coverage
        + settings.qualification_fit_capability_weight * breakdown.capability_coverage
        + settings.qualification_fit_structural_weight * breakdown.structural_score
    )
    assert breakdown.raw == pytest.approx(expected)


def test_calibrate_qualification_fit_display() -> None:
    assert calibrate_qualification_fit_display(0.5, raw_p5=0.2, raw_p95=0.7) == pytest.approx(0.6)
    assert calibrate_qualification_fit_display(0.1, raw_p5=0.2, raw_p95=0.7) == 0.0
    assert calibrate_qualification_fit_display(0.9, raw_p5=0.2, raw_p95=0.7) == 1.0
