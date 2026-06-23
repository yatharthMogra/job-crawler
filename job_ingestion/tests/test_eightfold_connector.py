from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.eightfold import EightfoldConnector
from app.ingestion.rate_limiter import reset_eightfold_buckets_for_tests
from app.models.company import Company

FIXTURES = Path(__file__).parent / "fixtures" / "eightfold"


@pytest.fixture(autouse=True)
def _reset_eightfold_buckets() -> None:
    reset_eightfold_buckets_for_tests()
    yield
    reset_eightfold_buckets_for_tests()


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _company(*, platform_config: dict[str, object] | None = None) -> Company:
    config = (
        {
            "api_host": "explore.jobs.netflix.net",
            "domain": "netflix.com",
        }
        if platform_config is None
        else platform_config
    )
    return Company(
        name="Netflix",
        platform="eightfold",
        board_token="netflix",
        is_active=True,
        platform_config=config,
    )


def _summary(
    job_id: str | int,
    *,
    job_description: str = "",
    name: str | None = None,
) -> dict[str, object]:
    return {
        "id": int(job_id) if str(job_id).isdigit() else job_id,
        "name": name or f"Role {job_id}",
        "location": "USA - Remote",
        "locations": ["USA - Remote"],
        "department": "Engineering",
        "job_description": job_description,
        "canonicalPositionUrl": f"https://explore.jobs.netflix.net/careers/job/{job_id}",
        "t_create": 1721692800,
    }


def _detail(job_id: str | int, *, description: str = "<p>Build APIs</p>") -> dict[str, object]:
    return {
        "id": int(job_id) if str(job_id).isdigit() else job_id,
        "name": f"Role {job_id}",
        "job_description": description,
        "canonicalPositionUrl": f"https://explore.jobs.netflix.net/careers/job/{job_id}",
    }


@pytest.mark.asyncio
async def test_pagination(monkeypatch) -> None:
    list_calls: list[dict[str, object]] = []
    detail_ids: list[str] = []

    class _FakeResponse:
        def __init__(
            self,
            payload: dict[str, object] | None = None,
            status_code: int = 200,
        ) -> None:
            self._payload = payload or {}
            self.status_code = status_code
            self.headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    "error",
                    request=httpx.Request("GET", "https://example.com"),
                    response=httpx.Response(self.status_code),
                )

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            if "/jobs/" in url and not url.endswith("/jobs"):
                job_id = url.rsplit("/", 1)[-1].split("?")[0]
                detail_ids.append(job_id)
                return _FakeResponse(_detail(job_id))
            start = (params or {}).get("start", 0)
            list_calls.append({"url": url, "start": start})
            if start == 0:
                return _FakeResponse(
                    {
                        "count": 15,
                        "positions": [_summary("790298014263")],
                    }
                )
            return _FakeResponse(
                {
                    "count": 15,
                    "positions": [_summary("790316506591")],
                }
            )

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _noop_sleep)

    jobs = await EightfoldConnector().fetch_jobs(_company())

    assert len(list_calls) == 2
    assert list_calls[0]["start"] == 0
    assert list_calls[1]["start"] == 10
    assert detail_ids == ["790298014263", "790316506591"]
    assert len(jobs) == 2
    assert jobs[0]["id"] == "790298014263"
    assert jobs[0]["job_description"] == "<p>Build APIs</p>"


@pytest.mark.asyncio
async def test_skip_detail_when_description_present(monkeypatch) -> None:
    detail_calls: list[str] = []

    class _FakeResponse:
        status_code = 200
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "count": 1,
                "positions": [
                    _summary(
                        "790298014263",
                        job_description="<p>Already here</p>",
                    )
                ],
            }

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            if "/jobs/" in url and not url.endswith("/jobs"):
                detail_calls.append(url)
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _noop_sleep)

    jobs = await EightfoldConnector().fetch_jobs(_company())

    assert detail_calls == []
    assert len(jobs) == 1
    assert jobs[0]["job_description"] == "<p>Already here</p>"


@pytest.mark.asyncio
async def test_detail_404_ingests_listing_without_description(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(
            self,
            payload: dict[str, object] | None = None,
            status_code: int = 200,
            headers: dict[str, str] | None = None,
        ) -> None:
            self._payload = payload
            self.status_code = status_code
            self.headers = headers or {}

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    "error",
                    request=httpx.Request("GET", "https://example.com"),
                    response=httpx.Response(self.status_code),
                )

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

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            if url.endswith("/790316506591"):
                return _FakeResponse(None, status_code=404)
            if "/jobs/" in url and not url.endswith("/jobs"):
                job_id = url.rsplit("/", 1)[-1].split("?")[0]
                return _FakeResponse(_detail(job_id))
            return _FakeResponse(
                {
                    "count": 2,
                    "positions": [_summary("790298014263"), _summary("790316506591")],
                }
            )

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _noop_sleep)

    jobs = await EightfoldConnector().fetch_jobs(_company())

    assert len(jobs) == 2
    by_id = {job["id"]: job for job in jobs}
    assert by_id["790298014263"]["job_description"] == "<p>Build APIs</p>"
    assert by_id["790316506591"]["job_description"] == ""
    assert by_id["790316506591"]["name"] == "Role 790316506591"


@pytest.mark.asyncio
async def test_zero_jobs(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"count": 0, "positions": []}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _noop_sleep)

    jobs = await EightfoldConnector().fetch_jobs(_company())
    assert jobs == []


@pytest.mark.asyncio
async def test_list_http_error(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200
        headers: dict[str, str] = {}

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

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _noop_sleep)

    with pytest.raises(ConnectorFetchError, match="Eightfold fetch failed for netflix"):
        await EightfoldConnector().fetch_jobs(_company())


@pytest.mark.asyncio
async def test_malformed_list(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"count": 0}

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _noop_sleep)

    with pytest.raises(ParseError, match="Malformed Eightfold list response"):
        await EightfoldConnector().fetch_jobs(_company())


def test_missing_platform_config_raises() -> None:
    company = _company(platform_config={})
    connector = EightfoldConnector()
    with pytest.raises(ParseError, match="Eightfold api_host missing"):
        connector._api_host(company)
    company_domain = Company(
        name="Netflix",
        platform="eightfold",
        board_token="netflix",
        is_active=True,
        platform_config={"api_host": "explore.jobs.netflix.net"},
    )
    with pytest.raises(ParseError, match="Eightfold domain missing"):
        connector._domain(company_domain)


@pytest.mark.asyncio
async def test_fixture_list_and_detail_shape() -> None:
    list_payload = json.loads((FIXTURES / "list_page.json").read_text())
    detail_payload = json.loads((FIXTURES / "detail_job.json").read_text())

    assert list_payload["count"] == 15
    assert len(list_payload["positions"]) == 2
    assert list_payload["positions"][0]["job_description"] == ""
    assert detail_payload["job_description"].startswith("<p>At Netflix")


@pytest.mark.asyncio
async def test_eightfold_partial_detail_failure_ingests_other_jobs(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(
            self,
            payload: dict[str, object] | None = None,
            *,
            status_code: int = 200,
            headers: dict[str, str] | None = None,
        ) -> None:
            self._payload = payload or {}
            self.status_code = status_code
            self.headers = headers or {}

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    "error",
                    request=httpx.Request("GET", "https://example.com"),
                    response=httpx.Response(self.status_code),
                )

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            if url.endswith("/790298014263"):
                return _FakeResponse(status_code=429)
            if "/jobs/" in url and not url.endswith("/jobs"):
                job_id = url.rsplit("/", 1)[-1].split("?")[0]
                return _FakeResponse(_detail(job_id, description=f"<p>{job_id}</p>"))
            return _FakeResponse(
                {
                    "count": 2,
                    "positions": [_summary("790298014263"), _summary("790316506591")],
                }
            )

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _noop_sleep)
    monkeypatch.setattr("app.ingestion.connectors.eightfold.EightfoldConnector.detail_retry_attempts", 1)

    jobs = await EightfoldConnector().fetch_jobs(_company())

    assert len(jobs) == 2
    by_id = {job["id"]: job for job in jobs}
    assert by_id["790316506591"]["job_description"] == "<p>790316506591</p>"
    assert by_id["790298014263"]["job_description"] == ""


@pytest.mark.asyncio
async def test_eightfold_detail_429_honors_retry_after(monkeypatch) -> None:
    detail_calls = 0
    sleep_calls: list[float] = []

    class _FakeResponse:
        def __init__(
            self,
            payload: dict[str, object] | None = None,
            *,
            status_code: int = 200,
            headers: dict[str, str] | None = None,
        ) -> None:
            self._payload = payload or {}
            self.status_code = status_code
            self.headers = headers or {}

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

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            nonlocal detail_calls
            if "/jobs/" in url and not url.endswith("/jobs"):
                detail_calls += 1
                if detail_calls == 1:
                    return _FakeResponse(status_code=429, headers={"Retry-After": "5"})
                job_id = url.rsplit("/", 1)[-1].split("?")[0]
                return _FakeResponse(_detail(job_id))
            return _FakeResponse(
                {
                    "count": 1,
                    "positions": [_summary("790298014263")],
                }
            )

    async def _record_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _record_sleep)

    jobs = await EightfoldConnector().fetch_jobs(_company())

    assert len(jobs) == 1
    assert jobs[0]["job_description"] == "<p>Build APIs</p>"
    assert detail_calls == 2
    assert 5.0 in sleep_calls


@pytest.mark.asyncio
async def test_eightfold_list_429_exponential_backoff(monkeypatch) -> None:
    list_calls = 0
    sleep_calls: list[float] = []

    class _FakeResponse:
        def __init__(
            self,
            payload: dict[str, object] | None = None,
            *,
            status_code: int = 200,
            headers: dict[str, str] | None = None,
        ) -> None:
            self._payload = payload or {}
            self.status_code = status_code
            self.headers = headers or {}

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

        async def get(self, url: str, params: dict[str, object] | None = None, **kwargs):  # noqa: ARG002
            nonlocal list_calls
            if url.endswith("/jobs"):
                list_calls += 1
                if list_calls == 1:
                    return _FakeResponse(status_code=429)
                return _FakeResponse({"count": 0, "positions": []})
            raise AssertionError("unexpected detail call")

    async def _record_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    monkeypatch.setattr(
        "app.ingestion.connectors.eightfold.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.eightfold.asyncio.sleep", _record_sleep)

    jobs = await EightfoldConnector().fetch_jobs(_company())

    assert jobs == []
    assert sleep_calls == [pytest.approx(2.0)]
