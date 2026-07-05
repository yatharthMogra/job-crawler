from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from app.models.shared import NormalizedJob
from app.notification.briefing_content import (
    build_job_card,
    detected_after,
    estimate_time_saved_minutes,
    format_salary,
)


def _job(**kwargs) -> NormalizedJob:
    now = datetime.now(timezone.utc)
    defaults = {
        "id": uuid.uuid4(),
        "title": "Software Engineer",
        "company_name": "Acme",
        "location": "New York, NY",
        "posting_url": "https://example.com",
        "posted_at": now - timedelta(hours=2),
        "reference_at": now - timedelta(hours=2),
        "is_active": True,
        "processing_state": "success",
        "seniority": "junior",
        "is_internship": False,
        "is_new_grad": False,
        "sponsorship_status": "yes",
        "sponsorship_confidence": "high",
        "remote_type": "hybrid",
        "tech_stack": ["Python"],
        "skills": ["REST"],
        "normalized_roles": ["SWE"],
        "job_capabilities": ["Backend Engineering"],
        "application_effort": "LOW",
        "retrieval_pools": ["SWE_FULLTIME"],
        "salary_min": 185_000,
        "salary_max": 225_000,
        "opportunity_score": 0.52,
        "created_at": now - timedelta(hours=1, minutes=54),
    }
    defaults.update(kwargs)
    return NormalizedJob(**defaults)


def test_format_salary_uses_k_suffix() -> None:
    assert format_salary(_job()) == "$185k - $225k"


def test_detected_after_uses_created_minus_posted() -> None:
    posted = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)
    created = datetime(2026, 6, 1, 12, 6, tzinfo=timezone.utc)
    job = _job(posted_at=posted, created_at=created)
    assert detected_after(job) == "6m after"


def test_build_job_card_apply_soon_on_last_rank() -> None:
    card = build_job_card(_job(), ["Python", "Backend Engineering"], 0.85, rank=4, total_jobs=4)
    assert card["cta"] == "APPLY SOON"
    assert card["rank_label"] == "04"
    assert card["market_signals"]


def test_estimate_time_saved() -> None:
    assert estimate_time_saved_minutes(25, 4) == 63
