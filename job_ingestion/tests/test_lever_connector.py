from __future__ import annotations

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.lever import LeverConnector
from app.models.company import Company


@pytest.mark.asyncio
async def test_lever_connector_fetches_jobs_from_public_v0(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> list[dict[str, object]]:
            return [
                {
                    "id": "job-1",
                    "text": "Software Engineer",
                    "hostedUrl": "https://jobs.lever.co/basis/job-1",
                    "createdAt": 1700000000000,
                    "categories": {"location": "Remote"},
                }
            ]

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object]):
            captured["url"] = url
            captured["params"] = params
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.lever.httpx.AsyncClient", _FakeClient)

    connector = LeverConnector()
    company = Company(name="Basis", platform="lever", board_token="basis", is_active=True)
    jobs = await connector.fetch_jobs(company)

    assert captured["url"] == "https://api.lever.co/v0/postings/basis"
    assert captured["params"] == {"mode": "json"}
    assert len(jobs) == 1
    assert jobs[0]["id"] == "job-1"


@pytest.mark.asyncio
async def test_lever_connector_raises_parse_error_for_malformed_payload(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"unexpected": "shape"}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object]):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.lever.httpx.AsyncClient", _FakeClient)

    connector = LeverConnector()
    company = Company(name="Basis", platform="lever", board_token="basis", is_active=True)
    with pytest.raises(ParseError, match="Malformed Lever response"):
        await connector.fetch_jobs(company)


@pytest.mark.asyncio
async def test_lever_connector_wraps_http_errors(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            raise RuntimeError("401 unauthorized")

        def json(self):  # pragma: no cover - not reached
            return []

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object]):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.lever.httpx.AsyncClient", _FakeClient)

    connector = LeverConnector()
    company = Company(name="Basis", platform="lever", board_token="basis", is_active=True)
    with pytest.raises(ConnectorFetchError, match="Lever fetch failed for basis"):
        await connector.fetch_jobs(company)
