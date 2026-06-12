from __future__ import annotations

import pytest

from app.exceptions import ConnectorFetchError, ParseError


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None
from app.ingestion.connectors.workday import WorkdayConnector
from app.models.company import Company


def _workday_company() -> Company:
    return Company(
        name="Stripe",
        platform="workday",
        board_token="stripe",
        platform_config={
            "tenant": "stripe",
            "instance": "wd1",
            "career_site": "External",
            "public_path_prefix": "External",
        },
        is_active=True,
    )


@pytest.mark.asyncio
async def test_workday_success_path(monkeypatch) -> None:
    captured: list[dict[str, object]] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | list[object], status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object] | list[object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: A002
            captured.append({"method": "post", "url": url, "json": json})
            return _FakeResponse(
                {
                    "total": 1,
                    "jobPostings": [
                        {
                            "title": "Senior Software Engineer",
                            "externalPath": "/job/New-York-NY-USA/Senior-Software-Engineer_JR-12345",
                            "locationsText": "New York, NY, USA",
                            "postedOn": "05/15/2026",
                            "bulletFields": ["Full time"],
                            "jobReqId": "JR-12345",
                        }
                    ],
                }
            )

        async def get(self, url: str):
            captured.append({"method": "get", "url": url})
            return _FakeResponse(
                {
                    "jobPostingInfo": {
                        "title": "Senior Software Engineer",
                        "jobReqId": "JR-12345",
                        "jobDescription": "<p>Build APIs with Python.</p>",
                        "location": "New York, NY, USA",
                        "postedOn": "05/15/2026",
                        "jobScheduleType": "Full_Time",
                        "department": "Engineering",
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())

    assert len(captured) == 2
    assert captured[0]["method"] == "post"
    assert captured[1]["method"] == "get"
    assert len(jobs) == 1
    assert jobs[0]["id"] == "JR-12345"
    assert jobs[0]["jobPostingInfo"]["jobDescription"] == "<p>Build APIs with Python.</p>"
    assert jobs[0]["externalLink"] == (
        "https://stripe.wd1.myworkdayjobs.com/External/job/New-York-NY-USA/Senior-Software-Engineer_JR-12345"
    )


@pytest.mark.asyncio
async def test_workday_pagination(monkeypatch) -> None:
    captured_offsets: list[int] = []

    class _FakeResponse:
        def __init__(self, payload: dict[str, object], status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

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
            offset = int(json["offset"])
            captured_offsets.append(offset)
            if offset == 0:
                return _FakeResponse(
                    {
                        "total": 25,
                            "jobPostings": [
                                {
                                    "title": f"Job {index}",
                                    "externalPath": f"/job/path-{index}",
                                    "jobReqId": f"JR-{index}",
                                    "postedOn": "Posted Today",
                                }
                                for index in range(20)
                            ],
                    }
                )
            return _FakeResponse(
                {
                    "total": 25,
                            "jobPostings": [
                                {
                                    "title": f"Job {index}",
                                    "externalPath": f"/job/path-{index}",
                                    "jobReqId": f"JR-{index}",
                                    "postedOn": "Posted Today",
                                }
                                for index in range(20, 25)
                            ],
                }
            )

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(
                {
                    "jobPostingInfo": {
                        "jobDescription": "<p>desc</p>",
                        "startDate": "2026-06-10",
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())

    assert captured_offsets == [0, 20]
    assert len(jobs) == 25


@pytest.mark.asyncio
async def test_workday_list_http_error(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 500

        def json(self) -> dict[str, object]:
            return {}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: ARG002, A002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)

    connector = WorkdayConnector()
    with pytest.raises(ConnectorFetchError, match="Workday list failed"):
        await connector.fetch_jobs(_workday_company())


@pytest.mark.asyncio
async def test_workday_detail_failure_includes_partial(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload or {}
            self.status_code = status_code

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: ARG002, A002
            return _FakeResponse(
                {
                    "total": 1,
                    "jobPostings": [
                        {
                            "title": "Software Engineer",
                            "externalPath": "/job/path-1",
                            "jobReqId": "JR-1",
                            "locationsText": "Remote",
                            "postedOn": "Posted Today",
                        }
                    ],
                }
            )

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(status_code=500)

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "JR-1"
    assert jobs[0]["title"] == "Software Engineer"
    assert jobs[0]["jobPostingInfo"] == {}


@pytest.mark.asyncio
async def test_workday_resolves_job_req_id_from_bullet_fields(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200

        def json(self) -> dict[str, object]:
            return {
                "total": 1,
                "jobPostings": [
                        {
                            "title": "Software Engineer",
                            "externalPath": "/job/Remote/SWE_JR-999",
                            "bulletFields": ["JR-999"],
                            "postedOn": "Posted Today",
                        }
                ],
            }

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: ARG002, A002
            return _FakeResponse()

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>desc</p>", "startDate": "2026-06-10"}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())
    assert len(jobs) == 1
    assert jobs[0]["id"] == "JR-999"


@pytest.mark.asyncio
async def test_workday_missing_job_req_id(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200

        def json(self) -> dict[str, object]:
            return {
                "total": 1,
                "jobPostings": [
                    {
                        "title": "Software Engineer",
                        "externalPath": "/job/path-1",
                    }
                ],
            }

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: ARG002, A002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())
    assert jobs == []


@pytest.mark.asyncio
async def test_workday_skips_jobs_older_than_30_days(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object], status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: ARG002, A002
            return _FakeResponse(
                {
                    "total": 2,
                    "jobPostings": [
                        {
                            "title": "Fresh role",
                            "externalPath": "/job/fresh",
                            "jobReqId": "JR-fresh",
                            "postedOn": "Posted Today",
                        },
                        {
                            "title": "Stale role",
                            "externalPath": "/job/stale",
                            "jobReqId": "JR-stale",
                            "postedOn": "Posted 30+ Days Ago",
                        },
                    ],
                }
            )

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(
                {
                    "jobPostingInfo": {
                        "jobDescription": "<p>desc</p>",
                        "startDate": "2026-06-10",
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())
    assert len(jobs) == 1
    assert jobs[0]["id"] == "JR-fresh"


@pytest.mark.asyncio
async def test_workday_malformed_list_json(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200

        def json(self) -> dict[str, object]:
            return {"total": 1, "jobPostings": "not-a-list"}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict[str, object]):  # noqa: ARG002, A002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)

    connector = WorkdayConnector()
    with pytest.raises(ParseError, match="missing jobPostings array"):
        await connector.fetch_jobs(_workday_company())
