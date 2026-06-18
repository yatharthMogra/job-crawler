from __future__ import annotations

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.workable import WorkableConnector
from app.models.company import Company


@pytest.mark.asyncio
async def test_workable_connector_fetches_jobs_with_details(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "jobs": [
                    {
                        "title": "AI Applications Engineer",
                        "shortcode": "48DBFB8E87",
                        "employment_type": "Full-time",
                        "department": "Software Engineering",
                        "url": "https://apply.workable.com/j/48DBFB8E87",
                        "published_on": "2025-08-25",
                        "telecommuting": False,
                        "locations": [
                            {
                                "country": "United States",
                                "city": "Burlingame",
                                "region": "California",
                            }
                        ],
                        "description": "Build AI applications on Quadric hardware.",
                    }
                ]
            }

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

    monkeypatch.setattr("app.ingestion.connectors.workable.httpx.AsyncClient", _FakeClient)

    connector = WorkableConnector()
    company = Company(
        name="Quadric",
        platform="workable",
        board_token="quadric-dot-i-o-inc",
        is_active=True,
    )
    jobs = await connector.fetch_jobs(company)

    assert captured["url"] == "https://apply.workable.com/api/v1/widget/accounts/quadric-dot-i-o-inc"
    assert captured["params"] == {"details": "true"}
    assert len(jobs) == 1
    assert jobs[0]["id"] == "48DBFB8E87"
    assert jobs[0]["shortcode"] == "48DBFB8E87"
    assert jobs[0]["description"] == "Build AI applications on Quadric hardware."


@pytest.mark.asyncio
async def test_workable_connector_dedupes_by_shortcode(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "jobs": [
                    {
                        "title": "Field Application Engineer (Machine Learning)",
                        "shortcode": "B463DB2082",
                        "telecommuting": True,
                        "locations": [{"country": "China", "countryCode": "CN"}],
                        "description": "Support customers in China.",
                    },
                    {
                        "title": "Field Application Engineer (Machine Learning)",
                        "shortcode": "B463DB2082",
                        "telecommuting": True,
                        "locations": [{"country": "Taiwan", "countryCode": "TW"}],
                        "description": "Support customers in Taiwan.",
                    },
                ]
            }

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object]):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.workable.httpx.AsyncClient", _FakeClient)

    connector = WorkableConnector()
    company = Company(
        name="Quadric",
        platform="workable",
        board_token="quadric-dot-i-o-inc",
        is_active=True,
    )
    jobs = await connector.fetch_jobs(company)

    assert len(jobs) == 1
    assert jobs[0]["id"] == "B463DB2082"
    assert len(jobs[0]["locations"]) == 2
    countries = {loc["country"] for loc in jobs[0]["locations"]}
    assert countries == {"China", "Taiwan"}


@pytest.mark.asyncio
async def test_workable_connector_raises_parse_error_for_malformed_payload(monkeypatch) -> None:
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

    monkeypatch.setattr("app.ingestion.connectors.workable.httpx.AsyncClient", _FakeClient)

    connector = WorkableConnector()
    company = Company(
        name="Quadric",
        platform="workable",
        board_token="quadric-dot-i-o-inc",
        is_active=True,
    )
    with pytest.raises(ParseError, match="Malformed Workable response"):
        await connector.fetch_jobs(company)


@pytest.mark.asyncio
async def test_workable_connector_wraps_http_errors(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            raise RuntimeError("404 not found")

        def json(self):  # pragma: no cover - not reached
            return {"jobs": []}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object]):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.workable.httpx.AsyncClient", _FakeClient)

    connector = WorkableConnector()
    company = Company(
        name="Quadric",
        platform="workable",
        board_token="quadric-dot-i-o-inc",
        is_active=True,
    )
    with pytest.raises(ConnectorFetchError, match="Workable fetch failed for quadric-dot-i-o-inc"):
        await connector.fetch_jobs(company)
