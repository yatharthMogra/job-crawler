from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.models.shared import NormalizedJob
from app.notification.ranker import (
    deduplicate_ranked_jobs,
    normalize_title,
    select_diversified_jobs,
    select_top_jobs,
)


def _job(title: str, company: str, location: str, score: float) -> tuple[NormalizedJob, float]:
    now = datetime.now(timezone.utc)
    job = NormalizedJob(
        id=uuid.uuid4(),
        title=title,
        company_name=company,
        location=location,
        posting_url="https://example.com",
        posted_at=now,
        reference_at=now,
        is_active=True,
        processing_state="success",
        seniority="junior",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="yes",
        sponsorship_confidence="high",
        remote_type="hybrid",
        tech_stack=[],
        skills=[],
        normalized_roles=[],
        job_capabilities=[],
        application_effort="LOW",
        retrieval_pools=[],
        salary_min=None,
        salary_max=None,
        opportunity_score=score,
        created_at=datetime.now(timezone.utc),
    )
    return job, score


def test_normalize_title_strips_whitespace_and_punctuation() -> None:
    assert normalize_title("  Software Engineer, Robotics.  ") == "software engineer, robotics"


def test_deduplicate_ranked_jobs_keeps_highest_score_first_occurrence() -> None:
    ranked = [
        _job("Software Engineer, Robotics", "Scale AI", "New York, NY", 0.9),
        _job("Software Engineer, Robotics", "Scale AI", "San Francisco, CA", 0.85),
        _job("Data Engineer", "Ramp", "New York, NY", 0.8),
    ]
    deduped = deduplicate_ranked_jobs(ranked)
    assert len(deduped) == 2
    assert deduped[0][0].location == "New York, NY"
    assert deduped[0][0].title == "Software Engineer, Robotics"
    assert deduped[1][0].title == "Data Engineer"


def test_deduplicate_ranked_jobs_allows_same_title_different_company() -> None:
    ranked = [
        _job("Software Engineer", "Scale AI", "New York, NY", 0.9),
        _job("Software Engineer", "Ramp", "New York, NY", 0.85),
    ]
    deduped = deduplicate_ranked_jobs(ranked)
    assert len(deduped) == 2


def test_select_top_jobs_caps_one_job_per_company() -> None:
    ranked = [
        _job("Data Scientist", "iSpot", "Remote", 0.9),
        _job("Research Data Scientist 1", "iSpot", "Bellevue, WA", 0.88),
        _job("Software Engineer II, Battery", "EnergyHub", "Remote", 0.85),
        _job("Software Engineer II, EV", "EnergyHub", "Remote", 0.84),
        _job("Backend Engineer", "Ramp", "New York, NY", 0.8),
    ]
    top = select_top_jobs(ranked, 4, max_per_company=1)
    assert len(top) == 3
    assert top[0][0].company_name == "iSpot"
    assert top[1][0].company_name == "EnergyHub"
    assert top[2][0].company_name == "Ramp"


def test_select_diversified_jobs_caps_company_share() -> None:
    ranked = [
        _job(f"Role {i}", "Amazon", "Remote", 0.9 - i * 0.01)
        for i in range(10)
    ] + [
        _job("Backend Engineer", "Ramp", "New York, NY", 0.5),
    ]
    selected = select_diversified_jobs(
        ranked,
        20,
        applied_count_by_company={},
        max_share=0.03,
        unlock_batch_size=5,
    )
    amazon_count = sum(1 for job, _ in selected if job.company_name == "Amazon")
    assert amazon_count == 1
    assert any(job.company_name == "Ramp" for job, _ in selected)


def test_select_diversified_jobs_unlocks_after_applies() -> None:
    ranked = [
        _job(f"Role {i}", "Amazon", "Remote", 0.9 - i * 0.01)
        for i in range(12)
    ] + [
        _job("Backend Engineer", "Ramp", "New York, NY", 0.5),
    ]
    selected = select_diversified_jobs(
        ranked,
        20,
        applied_count_by_company={"amazon": 5},
        max_share=0.03,
        unlock_batch_size=5,
    )
    amazon_count = sum(1 for job, _ in selected if job.company_name == "Amazon")
    assert amazon_count == 6
