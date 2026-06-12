from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.config import Settings
from app.models.shared import NormalizedJob
from app.notification.ranker import rank_jobs
from app.services.profile_loader import UserProfile


def _profile() -> UserProfile:
    return UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Test",
        constraints={},
        preferences={"preferred_locations": ["New York, NY"]},
        skills={"languages": ["Python"], "frameworks": [], "tools": [], "databases": [], "other": []},
        capabilities=[SimpleNamespace(capability_name="Backend Engineering")],
    )


def _job(*, posted_days_ago: int, opportunity_score: float) -> NormalizedJob:
    now = datetime.now(timezone.utc)
    return NormalizedJob(
        id=uuid.uuid4(),
        title="Backend Engineer",
        company_name="Acme",
        location="New York, NY",
        posting_url="https://example.com",
        posted_at=now - timedelta(days=posted_days_ago),
        is_active=True,
        processing_state="success",
        seniority="MID",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="yes",
        sponsorship_confidence="high",
        remote_type="hybrid",
        tech_stack=["Python"],
        skills=["REST"],
        normalized_roles=["BACKEND_ENGINEER"],
        job_capabilities=["Backend Engineering"],
        application_effort="LOW",
        retrieval_pools=["BACKEND_ENGINEER_FULLTIME"],
        salary_min=120_000,
        salary_max=150_000,
        opportunity_score=opportunity_score,
        created_at=now,
    )


def test_rank_jobs_prefers_fresher_posting_on_personal_score_tie() -> None:
    settings = Settings()
    profile = _profile()
    stale = _job(posted_days_ago=400, opportunity_score=0.52)
    fresh = _job(posted_days_ago=5, opportunity_score=0.32)
    ranked = rank_jobs([stale, fresh], profile, settings)
    assert ranked[0][0].id == fresh.id
    assert ranked[0][1] == ranked[1][1]
