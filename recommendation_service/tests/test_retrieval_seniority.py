from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

from app.config import Settings
from app.models.shared import NormalizedJob
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


def test_score_job_senior_penalty() -> None:
    settings = Settings()
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        constraints={"target_seniority": ["INTERN", "NEW_GRAD", "ENTRY", "MID"]},
        preferences={"preferred_locations": ["New York, NY"]},
        skills={"languages": ["Python"], "frameworks": [], "tools": [], "databases": [], "other": []},
        capabilities=[SimpleNamespace(capability_name="Backend Engineering")],
    )
    senior_score = score_job(_job(seniority="SENIOR", title="Senior Backend Engineer"), profile, settings)
    mid_score = score_job(_job(seniority="MID"), profile, settings)
    assert senior_score < mid_score

