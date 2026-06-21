from __future__ import annotations

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.bamboohr import BambooHRConnector, format_bamboohr_location
from app.models.company import Company


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _summary(job_id: str = "196") -> dict[str, object]:
    return {
        "id": job_id,
        "jobOpeningName": "Customer Support Rep",
        "departmentId": "18439",
        "departmentLabel": "Support",
        "employmentStatusLabel": "Full-Time",
        "location": {"city": None, "state": None},
        "atsLocation": {
            "country": "United States",
            "state": "Arizona",
            "city": "Phoenix",
        },
        "isRemote": None,
        "locationType": "1",
    }


def _detail(job_id: str = "196") -> dict[str, object]:
    return {
        "meta": {},
        "result": {
            "jobOpening": {
                "jobOpeningShareUrl": f"https://fullbay.bamboohr.com/careers/{job_id}",
                "jobOpeningName": "Customer Support Rep",
                "departmentLabel": "Support",
                "employmentStatusLabel": "Full-Time",
                "location": {"city": None, "state": None},
                "atsLocation": {
                    "country": "United States",
                    "state": "Arizona",
                    "city": "Phoenix",
                },
                "datePosted": "2026-01-07",
                "description": "<p>Handle incoming customer calls.</p>",
            }
        },
    }


def _company() -> Company:
    return Company(
        name="Fullbay",
        platform="bamboohr",
        board_token="fullbay",
        is_active=True,
    )


def test_format_bamboohr_location_prefers_ats_location() -> None:
    job = {
        "atsLocation": {"city": "Phoenix", "state": "Arizona", "country": "United States"},
        "location": {"city": "Bethesda", "state": "Maryland"},
    }
    assert format_bamboohr_location(job) == "Phoenix, Arizona, United States"


def test_format_bamboohr_location_falls_back_to_location() -> None:
    job = {
        "atsLocation": {"city": None, "state": None, "country": None},
        "location": {"city": "Bethesda", "state": "Maryland"},
    }
    assert format_bamboohr_location(job) == "Bethesda, Maryland"


def test_format_bamboohr_location_empty() -> None:
    assert format_bamboohr_location({}) is None


@pytest.mark.asyncio
async def test_fetch_jobs_success(monkeypatch) -> None:
    detail_ids: list[str] = []

    class _FakeResponse:
        def __init__(
            self,
            payload: dict[str, object] | None = None,
            status_code: int = 200,
        ) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise ConnectorFetchError(f"HTTP {self.status_code}")

        def json(self) -> dict[str, object]:
            assert self._payload is not None
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):  # noqa: ARG002
            if url.endswith("/careers/list"):
                return _FakeResponse({"meta": {"totalCount": 1}, "result": [_summary()]})
            if url.endswith("/detail"):
                job_id = url.rsplit("/", 2)[-2]
                detail_ids.append(job_id)
                return _FakeResponse(_detail(job_id))
            raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(
        "app.ingestion.connectors.bamboohr.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.bamboohr.asyncio.sleep", _noop_sleep)

    jobs = await BambooHRConnector().fetch_jobs(_company())

    assert detail_ids == ["196"]
    assert len(jobs) == 1
    assert jobs[0]["id"] == "196"
    assert jobs[0]["externalLink"] == "https://fullbay.bamboohr.com/careers/196"
    assert jobs[0]["description"] == "<p>Handle incoming customer calls.</p>"
    assert jobs[0]["datePosted"] == "2026-01-07"


@pytest.mark.asyncio
async def test_zero_jobs(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"meta": {"totalCount": 0}, "result": []}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.bamboohr.httpx.AsyncClient",
        _FakeClient,
    )

    jobs = await BambooHRConnector().fetch_jobs(_company())
    assert jobs == []


@pytest.mark.asyncio
async def test_detail_404_skipped(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object] | None = None, status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise ConnectorFetchError(f"HTTP {self.status_code}")

        def json(self) -> dict[str, object]:
            assert self._payload is not None
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):  # noqa: ARG002
            if url.endswith("/careers/list"):
                return _FakeResponse(
                    {
                        "meta": {"totalCount": 2},
                        "result": [_summary("ok"), _summary("missing")],
                    }
                )
            if url.endswith("/missing/detail"):
                return _FakeResponse(None, status_code=404)
            if url.endswith("/ok/detail"):
                return _FakeResponse(_detail("ok"))
            raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(
        "app.ingestion.connectors.bamboohr.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.bamboohr.asyncio.sleep", _noop_sleep)

    jobs = await BambooHRConnector().fetch_jobs(_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "ok"


@pytest.mark.asyncio
async def test_list_http_error(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            raise RuntimeError("503 unavailable")

        def json(self):  # pragma: no cover - not reached
            return {}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.bamboohr.httpx.AsyncClient",
        _FakeClient,
    )

    with pytest.raises(ConnectorFetchError, match="BambooHR list fetch failed for fullbay"):
        await BambooHRConnector().fetch_jobs(_company())


@pytest.mark.asyncio
async def test_malformed_list(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"meta": {"totalCount": 0}}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.bamboohr.httpx.AsyncClient",
        _FakeClient,
    )

    with pytest.raises(ParseError, match="Malformed BambooHR list response"):
        await BambooHRConnector().fetch_jobs(_company())
