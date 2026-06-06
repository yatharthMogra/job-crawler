from collections.abc import AsyncGenerator

from fastapi.testclient import TestClient

from app.api import pipeline as pipeline_api
from app.database import get_db
from app.ingestion.pipeline import PipelineSnapshot
from app.main import app


class DummySession:
    pass


async def _dummy_db() -> AsyncGenerator[DummySession, None]:
    yield DummySession()


def test_pipeline_trigger_smoke(monkeypatch) -> None:
    async def _fake_run_pipeline(db, run_type="manual", settings=None):  # noqa: ANN001
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
    async def _fake_run_pipeline(db, run_type="manual", settings=None):  # noqa: ANN001
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
