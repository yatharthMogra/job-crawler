from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.ingestion import pipeline
from app.ingestion.pipeline import CompanyRunOutcome
from app.models.pipeline_run import PipelineRun


@dataclass
class _FakeCompany:
    id: object
    name: str


class _ScalarResult:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows


class _FakeDbSession:
    def __init__(self, companies):
        self._companies = companies
        self._runs_by_id = {}
        self.commit_count = 0
        self.initial_commit_completed = False
        self.get_calls = 0

    def add(self, obj):
        if isinstance(obj, PipelineRun):
            self._runs_by_id[obj.id] = obj

    async def flush(self):
        return None

    async def commit(self):
        self.commit_count += 1
        if self.commit_count == 1:
            self.initial_commit_completed = True

    async def scalars(self, stmt):  # noqa: ARG002
        return _ScalarResult(self._companies)

    async def get(self, model, obj_id):  # noqa: ARG002
        self.get_calls += 1
        return self._runs_by_id.get(obj_id)


@pytest.mark.asyncio
async def test_run_pipeline_commits_parent_before_workers(monkeypatch) -> None:
    companies = [
        _FakeCompany(id=uuid4(), name="Anthropic"),
        _FakeCompany(id=uuid4(), name="Greenhouse"),
    ]
    fake_db = _FakeDbSession(companies=companies)
    settings = SimpleNamespace(fetch_concurrency=4)

    async def _fake_write_event(*args, **kwargs):  # noqa: ANN002, ANN003, ARG001
        return None

    async def _fake_process_single_company(company_id, pipeline_run_id, settings):  # noqa: ANN001
        assert fake_db.initial_commit_completed, "Workers must not run before initial run commit."
        return CompanyRunOutcome(
            company_id=company_id,
            status="success",
            jobs_fetched=1,
            jobs_new=1,
            jobs_updated=0,
            jobs_unchanged=0,
            jobs_removed=0,
        )

    monkeypatch.setattr(pipeline, "write_event", _fake_write_event)
    monkeypatch.setattr(pipeline, "_process_single_company", _fake_process_single_company)

    snapshot = await pipeline.run_pipeline(db=fake_db, run_type="manual", settings=settings)

    assert snapshot.status == "completed"
    assert snapshot.total_companies == 2
    assert snapshot.jobs_fetched == 2
    assert fake_db.commit_count == 2
    assert fake_db.get_calls == 1
