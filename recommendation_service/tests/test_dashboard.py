from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.api.dashboard import _job_to_out
from app.models.shared import NormalizedJob


def _job(**kwargs) -> NormalizedJob:
    defaults = {
        "id": uuid.uuid4(),
        "title": "Backend Engineer",
        "company_name": "Acme",
        "location": "New York, NY",
        "posting_url": "https://example.com/jobs/1",
        "description_text": "Build scalable backend services.",
        "description_preview": "Build scalable backend services.",
        "posted_at": datetime.now(timezone.utc),
        "is_active": True,
        "processing_state": "success",
        "seniority": "JUNIOR",
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
        "responsibilities": ["Build APIs"],
        "required_qualifications": ["Python"],
        "preferred_qualifications": [],
        "benefits": ["Equity"],
    }
    defaults.update(kwargs)
    return NormalizedJob(**defaults)


def test_job_to_out_includes_description_fields() -> None:
    out = _job_to_out(_job())
    assert out.description_text == "Build scalable backend services."
    assert out.description_preview == "Build scalable backend services."
    assert out.responsibilities == ["Build APIs"]
    assert out.required_qualifications == ["Python"]
    assert out.sponsorship_status == "yes"
    assert out.sponsorship_confidence == "high"


def test_job_to_out_handles_missing_description() -> None:
    out = _job_to_out(_job(description_text=None, description_preview=None))
    assert out.description_text is None
    assert out.description_preview is None
