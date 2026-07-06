from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.models.shared import NormalizedJob
from app.notification.renderer import render_daily_briefing
from app.services.profile_loader import UserProfile


def test_render_daily_briefing_includes_job_blocks() -> None:
    job = NormalizedJob(
        id=uuid.uuid4(),
        title="Backend Engineer",
        company_name="Acme",
        location="New York",
        posting_url="https://example.com/job",
        posted_at=datetime.now(timezone.utc),
        is_active=True,
        processing_state="success",
        seniority="junior",
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
        opportunity_score=0.9,
        created_at=datetime.now(timezone.utc),
    )
    profile = UserProfile(
        candidate_id=uuid.uuid4(),
        email="test@example.com",
        name="Alex",
        constraints={},
        preferences={},
        skills={},
    )
    html = render_daily_briefing(
        jobs_with_explanations=[(job, ["Python", "Backend Engineering"], 0.85)],
        user_profile=profile,
        total_scanned=12,
    )
    assert "PERSONALIZED DIGEST" in html
    assert "Backend Engineer" in html
    assert "Acme" in html
    assert "#01" in html
    assert "APPLY NOW" in html
    assert "PROFILE MATCH" in html
    assert "Why only 1 jobs?" in html
    assert f"/jobs/recommended?candidate_id={profile.candidate_id}" in html
    assert f"/emails?candidate_id={profile.candidate_id}" in html
    assert f"/unsubscribe?candidate_id={profile.candidate_id}" in html
    assert "channel=digest" in html
