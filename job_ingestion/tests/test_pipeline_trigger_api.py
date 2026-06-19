from collections.abc import AsyncGenerator
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import pipeline as pipeline_api
from app.database import get_db
from app.ingestion.pipeline import PipelineSnapshot
from app.main import app


class DummySession:
    pass


class _CompanyRow:
    def __init__(self) -> None:
        self.id = uuid4()


class _ScalarsResult:
    def __init__(self, rows: list[_CompanyRow]) -> None:
        self._rows = rows

    def all(self) -> list[_CompanyRow]:
        return self._rows


class FullScopeDb:
    async def scalars(self, stmt):  # noqa: ANN001, ARG002
        return _ScalarsResult([_CompanyRow(), _CompanyRow()])


async def _dummy_db() -> AsyncGenerator[DummySession, None]:
    yield DummySession()


def test_pipeline_trigger_full_scope(monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def _fake_run_pipeline(db, run_type="manual", settings=None, company_ids=None, schedule_metadata=None):  # noqa: ANN001
        captured["company_ids"] = company_ids
        captured["schedule_metadata"] = schedule_metadata
        return PipelineSnapshot(
            run_id="run-full",
            status="completed",
            total_companies=len(company_ids or []),
            successful_companies=len(company_ids or []),
            failed_companies=0,
            jobs_fetched=0,
            jobs_new=0,
            jobs_updated=0,
            jobs_unchanged=0,
            jobs_removed=0,
        )

    monkeypatch.setattr(pipeline_api, "run_pipeline", _fake_run_pipeline)

    async def _full_db() -> AsyncGenerator[FullScopeDb, None]:
        yield FullScopeDb()

    app.dependency_overrides[get_db] = _full_db
    client = TestClient(app)

    response = client.post("/pipeline/trigger?scope=full")
    assert response.status_code == 200
    assert len(captured["company_ids"]) == 2  # type: ignore[arg-type]
    assert captured["schedule_metadata"] == {"scope": "full", "companies_selected": 2}

    app.dependency_overrides.clear()


def test_pipeline_trigger_smoke(monkeypatch) -> None:
    async def _fake_run_pipeline(db, run_type="manual", settings=None, company_ids=None, schedule_metadata=None):  # noqa: ANN001
        return PipelineSnapshot(
            run_id="run-123",
            status="completed",
            total_companies=2,
            successful_companies=2,
            failed_companies=0,
            jobs_fetched=10,
            jobs_new=3,
            jobs_updated=2,
            jobs_unchanged=5,
            jobs_removed=0,
        )

    monkeypatch.setattr(pipeline_api, "run_pipeline", _fake_run_pipeline)
    app.dependency_overrides[get_db] = _dummy_db
    client = TestClient(app)

    response = client.post("/pipeline/trigger")
    assert response.status_code == 200
    assert response.json()["run_id"] == "run-123"
    assert response.json()["jobs_fetched"] == 10

    app.dependency_overrides.clear()


def test_pipeline_trigger_partial_success(monkeypatch) -> None:
    async def _fake_run_pipeline(db, run_type="manual", settings=None, company_ids=None, schedule_metadata=None):  # noqa: ANN001
        return PipelineSnapshot(
            run_id="run-partial",
            status="partial_success",
            total_companies=2,
            successful_companies=1,
            failed_companies=1,
            jobs_fetched=10,
            jobs_new=3,
            jobs_updated=2,
            jobs_unchanged=5,
            jobs_removed=0,
        )

    monkeypatch.setattr(pipeline_api, "run_pipeline", _fake_run_pipeline)
    app.dependency_overrides[get_db] = _dummy_db
    client = TestClient(app)

    response = client.post("/pipeline/trigger")
    assert response.status_code == 200
    assert response.json()["run_id"] == "run-partial"
    assert response.json()["status"] == "partial_success"

    app.dependency_overrides.clear()
