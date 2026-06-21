from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pytest

from app.exceptions import ConnectorFetchError, ParseError


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


from app.ingestion.connectors.workday import WorkdayConnector
from app.ingestion.job_freshness import workday_listing_recency_hint
from app.models.company import Company


def _recent_iso_date(days_ago: int = 1) -> str:
    return (datetime.now(timezone.utc).date() - timedelta(days=days_ago)).isoformat()


def _recent_us_date(days_ago: int = 1) -> str:
    posted = datetime.now(timezone.utc).date() - timedelta(days=days_ago)
    return posted.strftime("%m/%d/%Y")


def _workday_company(
  platform_config: dict[str, object] | None = None,
) -> Company:
    config: dict[str, object] = {
        "tenant": "stripe",
        "instance": "wd1",
        "career_site": "External",
        "public_path_prefix": "External",
    }
    if platform_config:
        config.update(platform_config)
    return Company(
        name="Stripe",
        platform="workday",
        board_token="stripe",
        platform_config=config,
        is_active=True,
    )


def _listing(posted_on: str, job_id: str) -> dict[str, object]:
    return {
        "title": f"Role {job_id}",
        "externalPath": f"/job/path-{job_id}",
        "jobReqId": job_id,
        "postedOn": posted_on,
    }


def _cached_job(
    job_id: str,
    *,
    title: str | None = None,
    external_path: str | None = None,
    description: str = "<p>desc</p>",
) -> dict[str, object]:
    return {
        "id": job_id,
        "title": title or f"Role {job_id}",
        "externalPath": external_path or f"/job/path-{job_id}",
        "postedOn": "Posted 5 Days Ago",
        "jobPostingInfo": {"jobDescription": description},
    }


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
                            "postedOn": _recent_us_date(3),
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
                        "postedOn": _recent_us_date(3),
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
                        "startDate": _recent_iso_date(1),
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
                {"jobPostingInfo": {"jobDescription": "<p>desc</p>", "startDate": _recent_iso_date(1)}}
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
    get_calls: list[str] = []

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

        async def get(self, url: str):
            get_calls.append(url)
            return _FakeResponse(
                {
                    "jobPostingInfo": {
                        "jobDescription": "<p>desc</p>",
                        "startDate": _recent_iso_date(1),
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())
    assert len(jobs) == 1
    assert jobs[0]["id"] == "JR-fresh"
    assert len(get_calls) == 1


def test_listing_recency_hint_custom_max_age() -> None:
    reference = datetime(2026, 6, 12, tzinfo=timezone.utc)
    hint = workday_listing_recency_hint

    assert hint("Posted 10 Days Ago", reference, 7) is False
    assert hint("Posted 10 Days Ago", reference, 30) is True
    assert hint("Posted 30+ Days Ago", reference, 30) is False
    assert hint("Posted 30+ Days Ago", reference, 45) is None
    assert hint("Posted 14+ Days Ago", reference, 30) is None
    assert hint("Posted Today", reference, 7) is True


@pytest.mark.asyncio
async def test_workday_stale_listings_skipped_during_accumulation(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload
            self.status_code = 200

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
                        _listing("Posted Today", "JR-fresh"),
                        _listing("Posted 30+ Days Ago", "JR-stale"),
                    ],
                }
            )

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse({"jobPostingInfo": {"jobDescription": "<p>x</p>"}})

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    company = _workday_company()
    listings = await connector._fetch_all_pages(
        connector._base_url(company),
        company,
        connector._max_posted_age_days(company),
        datetime(2026, 6, 12, tzinfo=timezone.utc),
    )
    assert [row["jobReqId"] for row in listings] == ["JR-fresh"]


@pytest.mark.asyncio
async def test_workday_no_early_stop_when_flag_false(monkeypatch) -> None:
    captured_offsets: list[int] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
            offset = int(json["offset"])
            captured_offsets.append(offset)
            if offset == 0:
                postings = [_listing("Posted Today", f"JR-{index}") for index in range(20)]
            elif offset == 20:
                postings = [
                    _listing("Posted 30+ Days Ago", f"JR-stale-{index}") for index in range(20)
                ]
            else:
                postings = [
                    _listing("Posted 30+ Days Ago", f"JR-stale-tail-{index}") for index in range(20)
                ]
            return _FakeResponse({"total": 100, "jobPostings": postings})

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>x</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(_workday_company())
    assert captured_offsets == [0, 20, 40, 60, 80]
    assert len(jobs) == 20


@pytest.mark.asyncio
async def test_workday_stops_after_two_consecutive_stale_pages(monkeypatch) -> None:
    captured_offsets: list[int] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
            offset = int(json["offset"])
            captured_offsets.append(offset)
            if offset == 0:
                postings = [_listing("Posted Today", f"JR-{index}") for index in range(20)]
            else:
                postings = [
                    _listing("Posted 30+ Days Ago", f"JR-stale-{offset}-{index}")
                    for index in range(20)
                ]
            return _FakeResponse({"total": 100, "jobPostings": postings})

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>x</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company({"stop_pagination_on_stale_tail": True})
    )
    assert captured_offsets == [0, 20, 40]
    assert len(jobs) == 20


@pytest.mark.asyncio
async def test_workday_no_early_stop_without_fresh_page(monkeypatch) -> None:
    captured_offsets: list[int] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
            offset = int(json["offset"])
            captured_offsets.append(offset)
            if offset == 0:
                postings = [
                    _listing("Posted 30+ Days Ago", f"JR-stale-{index}") for index in range(20)
                ]
            elif offset == 20:
                postings = [_listing("Posted Today", "JR-fresh")] + [
                    _listing("Posted 30+ Days Ago", f"JR-stale-tail-{index}")
                    for index in range(19)
                ]
            else:
                postings = [
                    _listing("Posted 30+ Days Ago", f"JR-stale-page-{offset}-{index}")
                    for index in range(20)
                ]
            return _FakeResponse({"total": 60, "jobPostings": postings})

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>x</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company({"stop_pagination_on_stale_tail": True})
    )
    assert captured_offsets == [0, 20, 40]
    assert len(jobs) == 1


@pytest.mark.asyncio
async def test_workday_consecutive_counter_resets_on_mixed_page(monkeypatch) -> None:
    captured_offsets: list[int] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
            offset = int(json["offset"])
            captured_offsets.append(offset)
            if offset == 0:
                postings = [_listing("Posted Today", "JR-fresh")]
            elif offset == 20:
                postings = [_listing("Posted 30+ Days Ago", "JR-stale-1")]
            elif offset == 40:
                postings = [
                    _listing("Posted Today", "JR-fresh-2"),
                    _listing("Posted 30+ Days Ago", "JR-stale-2"),
                ]
            else:
                postings = [
                    _listing("Posted 30+ Days Ago", f"JR-stale-tail-{offset}-{index}")
                    for index in range(20)
                ]
            return _FakeResponse({"total": 120, "jobPostings": postings})

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>x</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company({"stop_pagination_on_stale_tail": True})
    )
    assert captured_offsets == [0, 20, 40, 60, 80]
    assert len(jobs) == 2


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


def test_listing_fingerprint_ignores_posted_on() -> None:
    base = {"title": "Engineer", "locationsText": "Remote", "externalPath": "/job/a"}
    fp1 = WorkdayConnector._listing_fingerprint({**base, "postedOn": "Posted Today"})
    fp2 = WorkdayConnector._listing_fingerprint({**base, "postedOn": "Posted 5 Days Ago"})
    assert fp1 == fp2


@pytest.mark.asyncio
async def test_workday_incremental_skips_detail_for_cached_unchanged(monkeypatch) -> None:
    get_calls: list[str] = []

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
                    "total": 1,
                    "jobPostings": [_listing("Posted Today", "JR-1")],
                }
            )

        async def get(self, url: str):
            get_calls.append(url)
            return _FakeResponse({"jobPostingInfo": {"jobDescription": "<p>x</p>"}})

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    company = _workday_company({"workday_fetch_mode": "incremental"})
    jobs = await connector.fetch_jobs(
        company,
        known_raw_by_id={"JR-1": _cached_job("JR-1")},
        known_raw_fetched_at={"JR-1": datetime.now(timezone.utc) - timedelta(hours=1)},
    )
    assert len(jobs) == 1
    assert jobs[0]["id"] == "JR-1"
    assert get_calls == []


@pytest.mark.asyncio
async def test_workday_incremental_details_new_job(monkeypatch) -> None:
    get_calls: list[str] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
                {"total": 1, "jobPostings": [_listing("Posted Today", "JR-new")]}
            )

        async def get(self, url: str):
            get_calls.append(url)
            return _FakeResponse(
                {
                    "jobPostingInfo": {
                        "jobDescription": "<p>new</p>",
                        "startDate": _recent_iso_date(1),
                    }
                }
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company({"workday_fetch_mode": "incremental"}),
        known_raw_by_id={},
        known_raw_fetched_at={},
    )
    assert len(jobs) == 1
    assert len(get_calls) == 1


@pytest.mark.asyncio
async def test_workday_incremental_details_on_fingerprint_change(monkeypatch) -> None:
    get_calls: list[str] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
            listing = _listing("Posted Today", "JR-1")
            listing["title"] = "Updated title"
            return _FakeResponse({"total": 1, "jobPostings": [listing]})

        async def get(self, url: str):
            get_calls.append(url)
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>updated</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company({"workday_fetch_mode": "incremental"}),
        known_raw_by_id={"JR-1": _cached_job("JR-1")},
        known_raw_fetched_at={"JR-1": datetime(2026, 6, 11, tzinfo=timezone.utc)},
    )
    assert len(jobs) == 1
    assert len(get_calls) == 1


@pytest.mark.asyncio
async def test_workday_incremental_details_when_description_missing(monkeypatch) -> None:
    get_calls: list[str] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
                {"total": 1, "jobPostings": [_listing("Posted Today", "JR-1")]}
            )

        async def get(self, url: str):
            get_calls.append(url)
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>filled</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company({"workday_fetch_mode": "incremental"}),
        known_raw_by_id={"JR-1": _cached_job("JR-1", description="")},
        known_raw_fetched_at={"JR-1": datetime(2026, 6, 11, tzinfo=timezone.utc)},
    )
    assert len(jobs) == 1
    assert len(get_calls) == 1


@pytest.mark.asyncio
async def test_workday_incremental_refreshes_stale_cache(monkeypatch) -> None:
    get_calls: list[str] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
                {"total": 1, "jobPostings": [_listing("Posted Today", "JR-1")]}
            )

        async def get(self, url: str):
            get_calls.append(url)
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>refresh</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company(
            {"workday_fetch_mode": "incremental", "workday_full_refresh_days": 7}
        ),
        known_raw_by_id={"JR-1": _cached_job("JR-1")},
        known_raw_fetched_at={"JR-1": datetime(2026, 6, 1, tzinfo=timezone.utc)},
    )
    assert len(jobs) == 1
    assert len(get_calls) == 1


@pytest.mark.asyncio
async def test_workday_full_mode_unchanged(monkeypatch) -> None:
    get_calls: list[str] = []

    class _FakeResponse:
        status_code = 200

        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

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
                {"total": 1, "jobPostings": [_listing("Posted Today", "JR-1")]}
            )

        async def get(self, url: str):
            get_calls.append(url)
            return _FakeResponse(
                {"jobPostingInfo": {"jobDescription": "<p>x</p>", "startDate": _recent_iso_date(1)}}
            )

    monkeypatch.setattr("app.ingestion.connectors.workday.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.workday.asyncio.sleep", _noop_sleep)

    connector = WorkdayConnector()
    jobs = await connector.fetch_jobs(
        _workday_company(),
        known_raw_by_id={"JR-1": _cached_job("JR-1")},
        known_raw_fetched_at={"JR-1": datetime(2026, 6, 11, tzinfo=timezone.utc)},
    )
    assert len(jobs) == 1
    assert len(get_calls) == 1
