from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.oracle_hcm import OracleHCMConnector
from app.models.company import Company


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _oracle_company() -> Company:
    return Company(
        name="American Express",
        platform="oracle_hcm",
        board_token="egug",
        platform_config={
            "datacenter": "us2",
            "site_number": "CX_1",
        },
        is_active=True,
    )


def _recent_posted_date(days_ago: int = 0) -> str:
    return (datetime.now(timezone.utc).date() - timedelta(days=days_ago)).isoformat()


def _list_payload(
    jobs: list[dict[str, object]],
    *,
    total_jobs_count: int | None = None,
) -> dict[str, object]:
    enriched_jobs: list[dict[str, object]] = []
    for job in jobs:
        enriched = dict(job)
        if "PostedDate" not in enriched:
            enriched["PostedDate"] = _recent_posted_date()
        enriched_jobs.append(enriched)
    total = total_jobs_count if total_jobs_count is not None else len(enriched_jobs)
    return {
        "items": [
            {
                "TotalJobsCount": total,
                "requisitionList": enriched_jobs,
            }
        ],
        "hasMore": False,
    }


def _finder_offset(params: dict[str, object] | None) -> int:
    finder = str((params or {}).get("finder", ""))
    for key in ("offset=", "Offset="):
        if key in finder:
            return int(finder.split(key)[1].split(",")[0])
    return 0


def _detail_payload(job_id: str) -> dict[str, object]:
    return {
        "items": [
            {
                "Id": job_id,
                "Title": "Software Engineer III",
                "Category": "Information Technology",
                "ExternalDescriptionStr": "<p>Join our engineering team.</p>",
                "ExternalQualificationsStr": "<ul><li>5+ years Python</li></ul>",
                "ExternalResponsibilitiesStr": "<ul><li>Build scalable APIs</li></ul>",
                "WorkplaceType": "On-site",
                "requisitionFlexFields": [
                    {"Prompt": "Employment Type", "Value": "Full Time"},
                ],
            }
        ]
    }


@pytest.mark.asyncio
async def test_oracle_success_path(monkeypatch) -> None:
    captured: list[dict[str, object]] = []

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

        async def get(self, url: str, params: dict[str, object] | None = None, headers=None):  # noqa: ANN001
            captured.append({"url": url, "params": params, "headers": headers})
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse(
                    _list_payload(
                        [
                            {
                                "Id": "307750",
                                "Title": "Software Engineer III",
                                "PrimaryLocation": "New York, New York, United States",
                                "PostedDate": _recent_posted_date(1),
                            }
                        ]
                    )
                )
            return _FakeResponse(_detail_payload("307750"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "307750"
    assert jobs[0]["Id"] == "307750"
    assert jobs[0]["ExternalDescriptionStr"] == "<p>Join our engineering team.</p>"
    assert jobs[0]["externalLink"] == (
        "https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1"
        "/requisitions/307750/details"
    )
    assert len(captured) == 2
    assert "recruitingCEJobRequisitions" in captured[0]["url"]
    assert "recruitingCEJobRequisitionDetails" in captured[1]["url"]


@pytest.mark.asyncio
async def test_oracle_pagination_uses_finder_offset(monkeypatch) -> None:
    captured_finders: list[str] = []

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

        async def get(self, url: str, params: dict[str, object] | None = None, headers=None):  # noqa: ANN001, ARG002
            if "recruitingCEJobRequisitions" in url:
                finder = str((params or {}).get("finder", ""))
                captured_finders.append(finder)
                assert "limit" not in (params or {})
                assert "offset" not in (params or {})
                offset = _finder_offset(params)
                if offset == 0:
                    return _FakeResponse(
                        _list_payload(
                            [{"Id": str(index)} for index in range(25)],
                            total_jobs_count=50,
                        )
                    )
                return _FakeResponse(
                    _list_payload(
                        [{"Id": str(index)} for index in range(25, 50)],
                        total_jobs_count=50,
                    )
                )
            job_id = str((params or {}).get("finder", "")).split('Id="')[1].split('"')[0]
            return _FakeResponse(_detail_payload(job_id))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    listings = await connector._fetch_all_pages(
        "https://egug.fa.us2.oraclecloud.com/hcmRestApi/resources/latest",
        "CX_1",
    )

    assert captured_finders == [
        "findReqs;siteNumber=CX_1,offset=0,limit=100",
        "findReqs;siteNumber=CX_1,offset=25,limit=100",
    ]
    assert len(listings) == 50


@pytest.mark.asyncio
async def test_oracle_pagination(monkeypatch) -> None:
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

        async def get(self, url: str, params: dict[str, object] | None = None, headers=None):  # noqa: ANN001, ARG002
            if "recruitingCEJobRequisitions" in url:
                offset = _finder_offset(params)
                captured_offsets.append(offset)
                if offset == 0:
                    return _FakeResponse(
                        _list_payload(
                            [{"Id": str(index), "Title": f"Job {index}"} for index in range(100)],
                            total_jobs_count=101,
                        )
                    )
                return _FakeResponse(
                    _list_payload([{"Id": "100", "Title": "Job 100"}], total_jobs_count=101)
                )
            job_id = str((params or {}).get("finder", "")).split('Id="')[1].split('"')[0]
            return _FakeResponse(_detail_payload(job_id))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert captured_offsets == [0, 100]
    assert len(jobs) == 101


@pytest.mark.asyncio
async def test_oracle_nested_structure(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload or {
                "items": [
                    {
                        "TotalJobsCount": 1,
                        "requisitionList": [
                            {
                                "Id": "1",
                                "Title": "Nested Job",
                                "PostedDate": _recent_posted_date(),
                            }
                        ],
                    }
                ],
                "hasMore": False,
            }
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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse()
            return _FakeResponse(_detail_payload("1"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "1"


@pytest.mark.asyncio
async def test_oracle_sso_redirect(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 302

        def json(self) -> dict[str, object]:
            return {}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)

    connector = OracleHCMConnector()
    with pytest.raises(ConnectorFetchError, match="SSO-protected"):
        await connector.fetch_jobs(_oracle_company())


@pytest.mark.asyncio
async def test_oracle_detail_429_retry(monkeypatch) -> None:
    detail_attempts = 0

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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            nonlocal detail_attempts
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse(
                    _list_payload([{"Id": "307750", "Title": "Software Engineer III"}])
                )
            detail_attempts += 1
            if detail_attempts == 1:
                return _FakeResponse(status_code=429)
            return _FakeResponse(_detail_payload("307750"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert detail_attempts == 2
    assert len(jobs) == 1


@pytest.mark.asyncio
async def test_oracle_detail_failure_continues(monkeypatch) -> None:
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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse(
                    _list_payload(
                        [
                            {"Id": "1", "Title": "Fail Job"},
                            {"Id": "2", "Title": "Success Job"},
                        ]
                    )
                )
            finder = str((params or {}).get("finder", ""))
            if 'Id="1"' in finder:
                return _FakeResponse(status_code=500)
            return _FakeResponse(_detail_payload("2"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "2"


@pytest.mark.asyncio
async def test_oracle_missing_id(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload or _list_payload(
                [{"Title": "No ID Job"}, {"Id": "2", "Title": "Has ID"}]
            )
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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse()
            return _FakeResponse(_detail_payload("2"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "2"


@pytest.mark.asyncio
async def test_oracle_headers_present(monkeypatch) -> None:
    captured_headers: list[dict[str, str]] = []

    class _FakeResponse:
        status_code = 200

        def json(self) -> dict[str, object]:
            return _list_payload([])

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            if headers:
                captured_headers.append(headers)
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)

    connector = OracleHCMConnector()
    await connector.fetch_jobs(_oracle_company())

    assert len(captured_headers) == 1
    headers = captured_headers[0]
    assert headers["ora-irc-language"] == "en"
    assert headers["content-type"] == "application/vnd.oracle.adf.resourceitem+json;charset=utf-8"
    assert headers["ora-irc-cx-userid"]


@pytest.mark.asyncio
async def test_oracle_malformed_list_json(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200

        def json(self) -> dict[str, object]:
            raise ValueError("invalid json")

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)

    connector = OracleHCMConnector()
    with pytest.raises(ParseError, match="not valid JSON"):
        await connector.fetch_jobs(_oracle_company())


@pytest.mark.asyncio
async def test_oracle_skips_stale_from_list_posted_date(monkeypatch) -> None:
    detail_calls = 0

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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            nonlocal detail_calls
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse(
                    _list_payload(
                        [
                            {
                                "Id": "stale",
                                "Title": "Stale Job",
                                "PostedDate": _recent_posted_date(60),
                            }
                        ]
                    )
                )
            detail_calls += 1
            return _FakeResponse(_detail_payload("stale"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert jobs == []
    assert detail_calls == 0


@pytest.mark.asyncio
async def test_oracle_includes_recent_posted_date(monkeypatch) -> None:
    detail_calls = 0

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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            nonlocal detail_calls
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse(
                    _list_payload(
                        [
                            {
                                "Id": "fresh",
                                "Title": "Fresh Job",
                                "PostedDate": _recent_posted_date(1),
                            }
                        ]
                    )
                )
            detail_calls += 1
            return _FakeResponse(_detail_payload("fresh"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "fresh"
    assert detail_calls == 1


@pytest.mark.asyncio
async def test_oracle_post_detail_rejects_stale_when_list_date_missing(monkeypatch) -> None:
    detail_calls = 0

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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            nonlocal detail_calls
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse(
                    {
                        "items": [
                            {
                                "TotalJobsCount": 1,
                                "requisitionList": [{"Id": "1", "Title": "Undated on list"}],
                            }
                        ],
                        "hasMore": False,
                    }
                )
            detail_calls += 1
            payload = _detail_payload("1")
            payload["items"][0]["PostedDate"] = _recent_posted_date(60)  # type: ignore[index]
            return _FakeResponse(payload)

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(_oracle_company())

    assert jobs == []
    assert detail_calls == 1


@pytest.mark.asyncio
async def test_oracle_respects_max_posted_age_days_config(monkeypatch) -> None:
    company = Company(
        name="American Express",
        platform="oracle_hcm",
        board_token="egug",
        platform_config={
            "datacenter": "us2",
            "site_number": "CX_1",
            "max_posted_age_days": 7,
        },
        is_active=True,
    )

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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            if "recruitingCEJobRequisitions" in url:
                return _FakeResponse(
                    _list_payload(
                        [
                            {
                                "Id": "10d",
                                "Title": "Ten day old",
                                "PostedDate": _recent_posted_date(10),
                            }
                        ]
                    )
                )
            return _FakeResponse(_detail_payload("10d"))

    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.oracle_hcm.asyncio.sleep", _noop_sleep)

    connector = OracleHCMConnector()
    jobs = await connector.fetch_jobs(company)

    assert jobs == []
