from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api import manual_ingest as manual_ingest_api
from app.database import get_db
from app.main import app
from app.models.company import Company

FIXTURES = Path(__file__).parent / "fixtures" / "tesla_careers"
TESLA_ID = uuid4()


class _ScalarsResult:
    def __init__(self, rows: list) -> None:
        self._rows = rows

    def all(self) -> list:
        return self._rows


class TeslaIngestDb:
    def __init__(self, company: Company | None) -> None:
        self.company = company
        self.known_ids: list[str] = []

    async def get(self, _model, company_id):  # noqa: ANN001
        if self.company is not None and self.company.id == company_id:
            return self.company
        return None

    async def scalar(self, _stmt):  # noqa: ANN001
        return self.company

    async def scalars(self, _stmt):  # noqa: ANN001
        return _ScalarsResult(self.known_ids)


def _tesla_company() -> Company:
    return Company(
        id=TESLA_ID,
        name="Tesla",
        platform="tesla_careers",
        board_token="tesla",
        platform_config={"sites": ["US"], "ingestion_mode": "manual_push"},
        is_active=True,
        fetch_tier=3,
    )


def _state_payload() -> dict:
    return json.loads((FIXTURES / "state.json").read_text())


def test_manual_ingest_known_ids_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    db = TeslaIngestDb(_tesla_company())

    async def _get_db():
        yield db

    async def _known_ids(_db, _company_id):  # noqa: ANN001
        return []

    monkeypatch.setattr(manual_ingest_api, "get_known_external_ids", _known_ids)
    app.dependency_overrides[get_db] = _get_db
    client = TestClient(app)

    response = client.get("/ingest/tesla/known-ids")
    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_manual_ingest_plan_returns_pending_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    db = TeslaIngestDb(_tesla_company())

    async def _get_db():
        yield db

    async def _plan(_db, company, state_data):  # noqa: ANN001
        assert company.board_token == "tesla"
        return {
            "sites": ["US"],
            "listing_count": 2,
            "known_count": 1,
            "pending_detail_ids": ["221945"],
        }

    monkeypatch.setattr(manual_ingest_api, "plan_tesla_push", _plan)
    app.dependency_overrides[get_db] = _get_db
    client = TestClient(app)

    response = client.post("/ingest/tesla/plan", json={"state": _state_payload()})
    assert response.status_code == 200
    body = response.json()
    assert body["listing_count"] == 2
    assert body["pending_detail_ids"] == ["221945"]

    app.dependency_overrides.clear()


def test_manual_ingest_push_success(monkeypatch: pytest.MonkeyPatch) -> None:
    db = TeslaIngestDb(_tesla_company())

    async def _get_db():
        yield db

    async def _run_push(_db, company, state_data, details, *, settings):  # noqa: ANN001, ARG001
        from app.ingestion.pipeline import CompanyRunOutcome

        assert len(details) == 1
        return (
            CompanyRunOutcome(
                company_id=company.id,
                status="success",
                jobs_fetched=2,
                jobs_new=1,
                jobs_updated=0,
                jobs_unchanged=1,
            ),
            "run-123",
        )

    monkeypatch.setattr(manual_ingest_api, "run_tesla_manual_push", _run_push)
    app.dependency_overrides[get_db] = _get_db
    client = TestClient(app)

    detail = json.loads((FIXTURES / "detail_224501.json").read_text())
    response = client.post(
        "/ingest/tesla/push",
        json={"state": _state_payload(), "details": [detail]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "accepted"
    assert body["run_id"] == "run-123"
    assert body["jobs_new"] == 1
    assert body["jobs_unchanged"] == 1

    app.dependency_overrides.clear()


def test_manual_ingest_requires_token_when_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    db = TeslaIngestDb(_tesla_company())

    async def _get_db():
        yield db

    async def _known_ids(_db, _company_id):  # noqa: ANN001
        return []

    from app.config import Settings, get_settings

    settings = Settings(tesla_ingest_token="secret-token")

    monkeypatch.setattr(manual_ingest_api, "get_known_external_ids", _known_ids)
    app.dependency_overrides[get_db] = _get_db
    app.dependency_overrides[get_settings] = lambda: settings
    client = TestClient(app)

    response = client.get("/ingest/tesla/known-ids")
    assert response.status_code == 401

    response = client.get(
        "/ingest/tesla/known-ids",
        headers={"X-Ingest-Token": "secret-token"},
    )
    assert response.status_code == 200

    app.dependency_overrides.clear()
