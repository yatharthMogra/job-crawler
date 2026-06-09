from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


class _ScalarResult:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows


class _DummySession:
    def __init__(self, *, list_rows=None, detail_row=None, enrichments=None):
        self._list_rows = list_rows or []
        self._detail_row = detail_row
        self._enrichments = enrichments or []

    async def scalars(self, _stmt):
        if self._detail_row is not None:
            return _ScalarResult(self._enrichments)
        return _ScalarResult(self._list_rows)

    async def get(self, _model, _id):
        return self._detail_row


def _job_row() -> SimpleNamespace:
    now = datetime.now(UTC)
    return SimpleNamespace(
        id=uuid4(),
        raw_job_id=uuid4(),
        company_id=uuid4(),
        external_job_id="job-1",
        title="Backend Engineer",
        company_name="Acme",
        location="Remote",
        department="Engineering",
        employment_type="Full-time",
        posting_url="https://example.com/jobs/1",
        description_text="Full normalized description text for the job role.",
        description_preview="Full normalized description...",
        posted_at=now,
        is_active=True,
        consecutive_misses=0,
        last_seen_at=now,
        extraction_version="v1",
        llm_provider="gemini",
        llm_model="gemini-3.1-flash-lite",
        processing_state="success",
        failure_reason=None,
        extracted_at=now,
    )


def _enrichment_row() -> SimpleNamespace:
    now = datetime.now(UTC)
    return SimpleNamespace(
        id=uuid4(),
        status="success",
        failure_reason=None,
        llm_provider="gemini",
        llm_model="gemini-3.1-flash-lite",
        extraction_version="v1",
        seniority="mid",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="unclear",
        sponsorship_confidence="low",
        remote_type="remote",
        tech_stack=["python"],
        skills=["sql"],
        input_tokens=100,
        output_tokens=50,
        latency_ms=1000,
        created_at=now,
    )


def test_jobs_list_includes_description_preview() -> None:
    row = _job_row()
    session = _DummySession(list_rows=[row])

    async def _dummy_db() -> AsyncGenerator[_DummySession, None]:
        yield session

    app.dependency_overrides[get_db] = _dummy_db
    client = TestClient(app)

    response = client.get("/jobs?limit=1")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["description_preview"] == row.description_preview

    app.dependency_overrides.clear()


def test_job_detail_includes_description_text_and_preview() -> None:
    row = _job_row()
    enrichment = _enrichment_row()
    session = _DummySession(detail_row=row, enrichments=[enrichment])

    async def _dummy_db() -> AsyncGenerator[_DummySession, None]:
        yield session

    app.dependency_overrides[get_db] = _dummy_db
    client = TestClient(app)

    response = client.get(f"/jobs/{row.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["description_text"] == row.description_text
    assert body["description_preview"] == row.description_preview

    app.dependency_overrides.clear()
