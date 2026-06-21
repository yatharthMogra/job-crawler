from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from app.ingestion import pipeline
from app.models.company import Company
from app.models.pipeline_run import CompanyRunResult


@dataclass
class _FakeCompany:
    id: UUID
    name: str = "Amazon"
    platform: str = "amazon_jobs"
    board_token: str = "amazon"
    consecutive_fetch_failures: int = 0


class _FakeSession:
    def __init__(self, company: _FakeCompany) -> None:
        self.company = company
        self.rollback_count = 0
        self.committed = False
        self.added: list[object] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001
        return False

    async def get(self, model, obj_id):  # noqa: ANN001
        if model is Company and obj_id == self.company.id:
            return self.company
        return None

    async def rollback(self) -> None:
        self.rollback_count += 1

    def add(self, obj: object) -> None:
        self.added.append(obj)

    async def commit(self) -> None:
        self.committed = True


@pytest.mark.asyncio
async def test_process_single_company_rolls_back_before_recording_failure(monkeypatch) -> None:
    company_id = uuid4()
    run_id = uuid4()
    fake_company = _FakeCompany(id=company_id)
    fake_session = _FakeSession(fake_company)
    settings = SimpleNamespace(max_consecutive_failures_before_alert=3, alerts_path="/tmp/alerts.json")

    def _fake_session_local():
        return fake_session

    async def _noop_event(*args, **kwargs):  # noqa: ANN002, ANN003
        return None

    async def _empty_raw_map(db, cid):  # noqa: ANN001, ARG001
        return {}

    async def _fail_process(*args, **kwargs):  # noqa: ANN002, ANN003
        raise RuntimeError("value too long for type character varying(255)")

    async def _fetch_ok(*args, **kwargs):  # noqa: ANN002, ANN003
        return ([{"id": "1", "title": "Engineer"}], 0)

    monkeypatch.setattr(pipeline, "AsyncSessionLocal", _fake_session_local)
    monkeypatch.setattr(pipeline, "_latest_raw_by_external_id", _empty_raw_map)
    monkeypatch.setattr(pipeline, "_latest_raw_fetch_times", _empty_raw_map)
    monkeypatch.setattr(pipeline, "process_company_raw_jobs", _fail_process)
    monkeypatch.setattr(pipeline, "fetch_company_jobs", _fetch_ok)
    monkeypatch.setattr(pipeline, "write_event", _noop_event)
    monkeypatch.setattr(pipeline, "write_failure_alert", lambda **kwargs: None)

    outcome = await pipeline._process_single_company(
        company_id=company_id,
        pipeline_run_id=run_id,
        settings=settings,
    )

    assert outcome.status == "failed"
    assert "character varying(255)" in (outcome.error_message or "")
    assert fake_session.rollback_count == 1
    assert fake_company.consecutive_fetch_failures == 1
    assert fake_session.committed is True
    run_results = [obj for obj in fake_session.added if isinstance(obj, CompanyRunResult)]
    assert len(run_results) == 1
    assert run_results[0].error_message == outcome.error_message
