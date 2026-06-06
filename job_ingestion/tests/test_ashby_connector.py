from __future__ import annotations

import pytest

from app.exceptions import ParseError
from app.ingestion.connectors.ashby import AshbyConnector
from app.models.company import Company


@pytest.mark.asyncio
async def test_ashby_connector_fetches_jobs_via_graphql(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "data": {
                    "jobBoard": {
                        "jobPostings": [
                            {
                                "id": "job-1",
                                "title": "Software Engineer",
                                "locationName": "Remote",
                                "employmentType": "FullTime",
                            }
                        ]
                    }
                }
            }

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            captured["url"] = url
            captured["json"] = json
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)

    connector = AshbyConnector()
    company = Company(name="OpenAI", platform="ashby", board_token="openai", is_active=True)
    jobs = await connector.fetch_jobs(company)

    assert captured["url"] == "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
    assert captured["json"]["operationName"] == "ApiJobBoardWithTeams"
    assert captured["json"]["variables"]["organizationHostedJobsPageName"] == "openai"
    assert len(jobs) == 1
    assert jobs[0]["id"] == "job-1"
    assert jobs[0]["externalLink"] == "https://jobs.ashbyhq.com/openai/job-1"


@pytest.mark.asyncio
async def test_ashby_connector_raises_parse_error_on_graphql_errors(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"errors": [{"message": "Organization not found"}]}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: ARG002, A002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)

    connector = AshbyConnector()
    company = Company(name="OpenAI", platform="ashby", board_token="openai", is_active=True)

    with pytest.raises(ParseError, match="Ashby API returned errors"):
        await connector.fetch_jobs(company)
