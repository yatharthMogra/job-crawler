from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.ashby import AshbyConnector
from app.ingestion.rate_limiter import reset_ashby_bucket_for_tests
from app.models.company import Company


@pytest.fixture(autouse=True)
def _reset_ashby_bucket() -> None:
    reset_ashby_bucket_for_tests()
    yield
    reset_ashby_bucket_for_tests()


async def _noop_sleep(_: float) -> None:
    return None


def _ashby_company() -> Company:
    return Company(name="OpenAI", platform="ashby", board_token="openai", is_active=True)


@pytest.mark.asyncio
async def test_ashby_connector_fetches_jobs_with_description_html(monkeypatch) -> None:
    captured: list[dict[str, object]] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object], *, status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code
            self.headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            captured.append({"url": url, "json": json})
            operation = json.get("operationName")
            if operation == "ApiJobBoardWithTeams":
                return _FakeResponse(
                    {
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
                )
            if operation == "ApiJobPosting":
                return _FakeResponse(
                    {
                        "data": {
                            "jobPosting": {
                                "id": "job-1",
                                "title": "Software Engineer",
                                "locationName": "Remote",
                                "employmentType": "FullTime",
                                "descriptionHtml": "<p>Build APIs with Python.</p>",
                                "publishedDate": "2026-01-01T00:00:00.000Z",
                                "departmentName": "Engineering",
                            }
                        }
                    }
                )
            raise AssertionError(f"unexpected operation: {operation}")

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(_ashby_company())

    assert len(captured) == 2
    assert captured[0]["json"]["operationName"] == "ApiJobBoardWithTeams"
    assert captured[1]["json"]["operationName"] == "ApiJobPosting"
    assert len(jobs) == 1
    assert jobs[0]["id"] == "job-1"
    assert jobs[0]["descriptionHtml"] == "<p>Build APIs with Python.</p>"
    assert jobs[0]["externalLink"] == "https://jobs.ashbyhq.com/openai/job-1"


@pytest.mark.asyncio
async def test_ashby_connector_raises_parse_error_on_graphql_errors(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200
        headers: dict[str, str] = {}

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
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)

    connector = AshbyConnector()

    with pytest.raises(ParseError, match="Ashby API returned errors"):
        await connector.fetch_jobs(_ashby_company())


@pytest.mark.asyncio
async def test_ashby_detail_429_retry_after(monkeypatch) -> None:
    detail_calls = 0
    sleep_calls: list[float] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, *, status_code: int = 200) -> None:
            self._payload = payload or {}
            self.status_code = status_code
            self.headers = {"Retry-After": "2"} if status_code == 429 else {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            nonlocal detail_calls
            if json.get("operationName") == "ApiJobBoardWithTeams":
                return _FakeResponse(
                    {
                        "data": {
                            "jobBoard": {
                                "jobPostings": [
                                    {
                                        "id": "job-1",
                                        "title": "Engineer",
                                        "locationName": "Remote",
                                        "employmentType": "FullTime",
                                    }
                                ]
                            }
                        }
                    }
                )
            detail_calls += 1
            if detail_calls == 1:
                return _FakeResponse(status_code=429)
            return _FakeResponse(
                {
                    "data": {
                        "jobPosting": {
                            "id": "job-1",
                            "descriptionHtml": "<p>Hello</p>",
                        }
                    }
                }
            )

    async def _record_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _record_sleep)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(_ashby_company())

    assert len(jobs) == 1
    assert 2.0 in sleep_calls
    assert detail_calls == 2


@pytest.mark.asyncio
async def test_ashby_list_429_exponential_backoff(monkeypatch) -> None:
    list_calls = 0
    sleep_calls: list[float] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, *, status_code: int = 200) -> None:
            self._payload = payload or {}
            self.status_code = status_code
            self.headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            nonlocal list_calls
            if json.get("operationName") == "ApiJobBoardWithTeams":
                list_calls += 1
                if list_calls == 1:
                    return _FakeResponse(status_code=429)
                return _FakeResponse({"data": {"jobBoard": {"jobPostings": []}}})
            raise AssertionError("unexpected detail call")

    async def _record_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _record_sleep)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(_ashby_company())

    assert jobs == []
    assert sleep_calls == [pytest.approx(2.0)]


@pytest.mark.asyncio
async def test_ashby_partial_detail_failure_ingests_other_jobs(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, *, status_code: int = 200) -> None:
            self._payload = payload or {}
            self.status_code = status_code
            self.headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            operation = json.get("operationName")
            if operation == "ApiJobBoardWithTeams":
                return _FakeResponse(
                    {
                        "data": {
                            "jobBoard": {
                                "jobPostings": [
                                    {
                                        "id": "job-1",
                                        "title": "One",
                                        "locationName": "Remote",
                                        "employmentType": "FullTime",
                                    },
                                    {
                                        "id": "job-2",
                                        "title": "Two",
                                        "locationName": "Remote",
                                        "employmentType": "FullTime",
                                    },
                                ]
                            }
                        }
                    }
                )
            job_id = json["variables"]["jobPostingId"]
            if job_id == "job-1":
                return _FakeResponse(status_code=429)
            return _FakeResponse(
                {
                    "data": {
                        "jobPosting": {
                            "id": "job-2",
                            "descriptionHtml": "<p>Two</p>",
                        }
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)
    monkeypatch.setattr("app.ingestion.connectors.ashby.AshbyConnector.detail_retry_attempts", 1)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(_ashby_company())

    assert len(jobs) == 2
    by_id = {job["id"]: job for job in jobs}
    assert by_id["job-2"]["descriptionHtml"] == "<p>Two</p>"
    assert "descriptionHtml" not in by_id["job-1"]


@pytest.mark.asyncio
async def test_ashby_detail_failure_uses_cache_fallback(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 429
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            if json.get("operationName") == "ApiJobBoardWithTeams":
                return type(
                    "_ListResponse",
                    (),
                    {
                        "status_code": 200,
                        "headers": {},
                        "raise_for_status": lambda self: None,
                        "json": lambda self: {
                            "data": {
                                "jobBoard": {
                                    "jobPostings": [
                                        {
                                            "id": "job-1",
                                            "title": "Engineer",
                                            "locationName": "Remote",
                                            "employmentType": "FullTime",
                                        }
                                    ]
                                }
                            }
                        },
                    },
                )()
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)
    monkeypatch.setattr("app.ingestion.connectors.ashby.AshbyConnector.detail_retry_attempts", 1)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(
        _ashby_company(),
        known_raw_by_id={
            "job-1": {
                "id": "job-1",
                "title": "Engineer",
                "locationName": "Remote",
                "employmentType": "FullTime",
                "descriptionHtml": "<p>Cached description</p>",
            }
        },
    )

    assert len(jobs) == 1
    assert jobs[0]["descriptionHtml"] == "<p>Cached description</p>"


@pytest.mark.asyncio
async def test_ashby_all_details_fail_raises(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 429
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            if json.get("operationName") == "ApiJobBoardWithTeams":
                return type(
                    "_ListResponse",
                    (),
                    {
                        "status_code": 200,
                        "headers": {},
                        "raise_for_status": lambda self: None,
                        "json": lambda self: {
                            "data": {
                                "jobBoard": {
                                    "jobPostings": [
                                        {
                                            "id": "job-1",
                                            "title": "Engineer",
                                            "locationName": "Remote",
                                            "employmentType": "FullTime",
                                        }
                                    ]
                                }
                            }
                        },
                    },
                )()
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)
    monkeypatch.setattr("app.ingestion.connectors.ashby.AshbyConnector.detail_retry_attempts", 1)

    connector = AshbyConnector()

    with pytest.raises(ConnectorFetchError, match="failed for all jobs"):
        await connector.fetch_jobs(_ashby_company())


@pytest.mark.asyncio
async def test_ashby_incremental_skips_unchanged_detail(monkeypatch) -> None:
    captured: list[str] = []

    class _FakeResponse:
        status_code = 200
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "data": {
                    "jobBoard": {
                        "jobPostings": [
                            {
                                "id": "job-1",
                                "title": "Engineer",
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
            captured.append(str(json.get("operationName")))
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(
        _ashby_company(),
        known_raw_by_id={
            "job-1": {
                "id": "job-1",
                "title": "Engineer",
                "locationName": "Remote",
                "employmentType": "FullTime",
                "descriptionHtml": "<p>Cached</p>",
            }
        },
        known_raw_fetched_at={"job-1": datetime.now(timezone.utc) - timedelta(hours=1)},
    )

    assert captured == ["ApiJobBoardWithTeams"]
    assert len(jobs) == 1
    assert jobs[0]["descriptionHtml"] == "<p>Cached</p>"


@pytest.mark.asyncio
async def test_ashby_incremental_refetches_on_listing_change(monkeypatch) -> None:
    captured: list[str] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self.status_code = 200
            self.headers: dict[str, str] = {}
            self._payload = payload

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            captured.append(str(json.get("operationName")))
            if json.get("operationName") == "ApiJobBoardWithTeams":
                return _FakeResponse(
                    {
                        "data": {
                            "jobBoard": {
                                "jobPostings": [
                                    {
                                        "id": "job-1",
                                        "title": "Senior Engineer",
                                        "locationName": "Remote",
                                        "employmentType": "FullTime",
                                    }
                                ]
                            }
                        }
                    }
                )
            return _FakeResponse(
                {
                    "data": {
                        "jobPosting": {
                            "id": "job-1",
                            "title": "Senior Engineer",
                            "descriptionHtml": "<p>Updated</p>",
                        }
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(
        _ashby_company(),
        known_raw_by_id={
            "job-1": {
                "id": "job-1",
                "title": "Engineer",
                "locationName": "Remote",
                "employmentType": "FullTime",
                "descriptionHtml": "<p>Cached</p>",
            }
        },
        known_raw_fetched_at={"job-1": datetime.now(timezone.utc) - timedelta(hours=1)},
    )

    assert captured == ["ApiJobBoardWithTeams", "ApiJobPosting"]
    assert jobs[0]["descriptionHtml"] == "<p>Updated</p>"


@pytest.mark.asyncio
async def test_ashby_incremental_refetches_stale_cache(monkeypatch) -> None:
    captured: list[str] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self.status_code = 200
            self.headers: dict[str, str] = {}
            self._payload = payload

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            captured.append(str(json.get("operationName")))
            if json.get("operationName") == "ApiJobBoardWithTeams":
                return _FakeResponse(
                    {
                        "data": {
                            "jobBoard": {
                                "jobPostings": [
                                    {
                                        "id": "job-1",
                                        "title": "Engineer",
                                        "locationName": "Remote",
                                        "employmentType": "FullTime",
                                    }
                                ]
                            }
                        }
                    }
                )
            return _FakeResponse(
                {
                    "data": {
                        "jobPosting": {
                            "id": "job-1",
                            "descriptionHtml": "<p>Refreshed</p>",
                        }
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.ashby.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.ashby.asyncio.sleep", _noop_sleep)

    connector = AshbyConnector()
    jobs = await connector.fetch_jobs(
        _ashby_company(),
        known_raw_by_id={
            "job-1": {
                "id": "job-1",
                "title": "Engineer",
                "locationName": "Remote",
                "employmentType": "FullTime",
                "descriptionHtml": "<p>Cached</p>",
            }
        },
        known_raw_fetched_at={"job-1": datetime.now(timezone.utc) - timedelta(days=8)},
    )

    assert captured == ["ApiJobBoardWithTeams", "ApiJobPosting"]
    assert jobs[0]["descriptionHtml"] == "<p>Refreshed</p>"
