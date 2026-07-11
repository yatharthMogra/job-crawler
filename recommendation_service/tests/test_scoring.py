from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.explainability import generate_explanations
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
        "seniority": "JUNIOR",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "yes",
        "sponsorship_confidence": "high",
        "remote_type": "hybrid",
        "tech_stack": ["Python", "AWS"],
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


def test_score_job_capability_overlap() -> None:
    settings = Settings()
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        constraints={},
        preferences={"preferred_locations": ["New York, NY"]},
        skills={"languages": ["Python"], "frameworks": [], "tools": [], "databases": [], "other": []},
        capabilities=[SimpleNamespace(capability_name="Backend Engineering")],
    )
    job = _job(required_skills=["Python"], job_capabilities=["Backend Engineering"])
    score = score_job(job, profile, settings)
    assert score > 0.55


def test_score_job_respects_minimum_salary() -> None:
    settings = Settings()
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        constraints={"minimum_salary": 200_000},
        preferences={},
        skills={},
        capabilities=[],
    )
    low_pay_job = _job(salary_min=80_000, salary_max=90_000)
    score = score_job(low_pay_job, profile, settings)
    assert score < 0.6


def test_generate_explanations_includes_capabilities_and_skills() -> None:
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        constraints={},
        preferences={},
        skills={"languages": ["Python"], "frameworks": [], "tools": [], "databases": [], "other": []},
        capabilities=[SimpleNamespace(capability_name="Backend Engineering")],
    )
    job = _job()
    reasons = generate_explanations(job, profile)
    assert "Backend Engineering" in reasons
    assert "Python" in reasons
