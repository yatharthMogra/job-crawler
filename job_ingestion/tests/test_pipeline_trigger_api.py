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

    async def _fake_run_pipeline(  # noqa: ANN001
        db,
        run_type="manual",
        settings=None,
        company_ids=None,
        schedule_metadata=None,
        force=False,
    ):
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


def test_pipeline_trigger_force_param(monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def _fake_run_pipeline(  # noqa: ANN001
        db,
        run_type="manual",
        settings=None,
        company_ids=None,
        schedule_metadata=None,
        force=False,
    ):
        captured["force"] = force
        return PipelineSnapshot(
            run_id="run-force",
            status="completed",
            total_companies=0,
            successful_companies=0,
            failed_companies=0,
            jobs_fetched=0,
            jobs_new=0,
            jobs_updated=0,
            jobs_unchanged=0,
            jobs_removed=0,
        )

    monkeypatch.setattr(pipeline_api, "run_pipeline", _fake_run_pipeline)
    app.dependency_overrides[get_db] = _dummy_db
    client = TestClient(app)

    response = client.post("/pipeline/trigger", params={"force": True})
    assert response.status_code == 200
    assert captured["force"] is True

    app.dependency_overrides.clear()


def test_pipeline_trigger_smoke(monkeypatch) -> None:
    async def _fake_run_pipeline(  # noqa: ANN001
        db,
        run_type="manual",
        settings=None,
        company_ids=None,
        schedule_metadata=None,
        force=False,
    ):
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


def test_pipeline_trigger_single_company(monkeypatch) -> None:
    captured: dict[str, object] = {}
    company = _CompanyRow()

    async def _fake_run_pipeline(  # noqa: ANN001
        db,
        run_type="manual",
        settings=None,
        company_ids=None,
        schedule_metadata=None,
        force=False,
    ):
        captured["company_ids"] = company_ids
        captured["schedule_metadata"] = schedule_metadata
        captured["force"] = force
        return PipelineSnapshot(
            run_id="run-single",
            status="completed",
            total_companies=1,
            successful_companies=1,
            failed_companies=0,
            jobs_fetched=100,
            jobs_new=100,
            jobs_updated=0,
            jobs_unchanged=0,
            jobs_removed=0,
        )

    class _SingleCompanyDb:
        async def get(self, _model, company_uuid):  # noqa: ANN001, ARG002
            if company_uuid == company.id:
                row = _CompanyRow()
                row.id = company.id
                row.name = "Google"
                row.is_active = True
                return row
            return None

    monkeypatch.setattr(pipeline_api, "run_pipeline", _fake_run_pipeline)

    async def _single_db() -> AsyncGenerator[_SingleCompanyDb, None]:
        yield _SingleCompanyDb()

    app.dependency_overrides[get_db] = _single_db
    client = TestClient(app)

    response = client.post("/pipeline/trigger", params={"company_id": str(company.id), "force": True})
    assert response.status_code == 200
    assert captured["company_ids"] == [company.id]
    assert captured["schedule_metadata"] == {
        "scope": "single",
        "company_id": str(company.id),
        "company_name": "Google",
        "companies_selected": 1,
    }
    assert captured["force"] is True
    assert response.json()["jobs_fetched"] == 100

    app.dependency_overrides.clear()


def test_pipeline_trigger_single_company_not_found() -> None:
    class _EmptyDb:
        async def get(self, _model, _company_uuid):  # noqa: ANN001
            return None

    async def _empty_db() -> AsyncGenerator[_EmptyDb, None]:
        yield _EmptyDb()

    app.dependency_overrides[get_db] = _empty_db
    client = TestClient(app)

    response = client.post("/pipeline/trigger", params={"company_id": str(uuid4())})
    assert response.status_code == 404

    app.dependency_overrides.clear()


def test_pipeline_trigger_single_company_rejects_full_scope() -> None:
    app.dependency_overrides[get_db] = _dummy_db
    client = TestClient(app)

    response = client.post(
        "/pipeline/trigger",
        params={"company_id": str(uuid4()), "scope": "full"},
    )
    assert response.status_code == 400

    app.dependency_overrides.clear()


def test_pipeline_trigger_partial_success(monkeypatch) -> None:
    async def _fake_run_pipeline(  # noqa: ANN001
        db,
        run_type="manual",
        settings=None,
        company_ids=None,
        schedule_metadata=None,
        force=False,
    ):
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
