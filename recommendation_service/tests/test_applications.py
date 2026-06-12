from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services.applications import format_application_row


def test_format_application_prefers_archive_data() -> None:
    application = SimpleNamespace(
        id=uuid4(),
        candidate_id=uuid4(),
        job_archive_id=uuid4(),
        company_name="Denorm Co",
        job_title="Denorm Title",
        location="Denorm Loc",
        platform="greenhouse",
        external_job_id="123",
        applied_at=datetime.now(timezone.utc),
        status="applied",
        notes=None,
    )
    archive = SimpleNamespace(
        company_name="Archive Co",
        title="Archive Title",
        location="Archive Loc",
        platform="workday",
        external_job_id="123",
        posting_url="https://example.com",
        salary_min=100000,
        salary_max=150000,
        seniority="senior",
        skills=["python"],
        tech_stack=["postgres"],
        description_text="Job description",
    )
    out = format_application_row(application, archive=archive, normalized_job_id=uuid4())
    assert out.company_name == "Archive Co"
    assert out.job_title == "Archive Title"
    assert out.description_text == "Job description"
    assert out.skills == ["python"]


def test_format_application_falls_back_when_archive_missing() -> None:
    application = SimpleNamespace(
        id=uuid4(),
        candidate_id=uuid4(),
        job_archive_id=None,
        company_name="Denorm Co",
        job_title="Denorm Title",
        location="Denorm Loc",
        platform="greenhouse",
        external_job_id="123",
        applied_at=datetime.now(timezone.utc),
        status="applied",
        notes="note",
    )
    out = format_application_row(application, archive=None)
    assert out.company_name == "Denorm Co"
    assert out.job_title == "Denorm Title"
    assert out.description_text is None


@pytest.mark.asyncio
async def test_apply_to_job_requires_archive_id() -> None:
    from fastapi import HTTPException

    from app.services.applications import apply_to_job

    job = SimpleNamespace(
        id=uuid4(),
        job_archive_id=None,
        company_id=uuid4(),
        company_name="Acme",
        title="Engineer",
        location="Remote",
        external_job_id="ext-1",
    )
    db = AsyncMock()
    db.scalar = AsyncMock(return_value=job)

    with pytest.raises(HTTPException) as exc:
        await apply_to_job(db, candidate_id=uuid4(), job_id=job.id)
    assert exc.value.status_code == 404
