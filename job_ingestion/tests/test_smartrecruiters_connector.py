from __future__ import annotations

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.smartrecruiters import SmartRecruitersConnector
from app.models.company import Company


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _summary(job_id: str, *, remote: bool = False) -> dict[str, object]:
    return {
        "id": job_id,
        "name": f"Role {job_id}",
        "releasedDate": "2026-06-01T15:28:46.493Z",
        "location": {
            "city": "North Chicago",
            "region": "Illinois",
            "country": "us",
            "remote": remote,
        },
    }


def _detail(job_id: str, *, sections: dict[str, object] | None = None) -> dict[str, object]:
    default_sections = {
        "companyDescription": {"text": "<p>About us</p>"},
        "jobDescription": {"text": "<p>Build APIs</p>"},
        "qualifications": {"text": "<p>5 years experience</p>"},
        "additionalInformation": {"text": "<p>Benefits</p>"},
    }
    return {
        "id": job_id,
        "name": f"Role {job_id}",
        "jobAd": {"sections": sections if sections is not None else default_sections},
    }


def _company() -> Company:
    return Company(
        name="AbbVie",
        platform="smartrecruiters",
        board_token="abbvie",
        is_active=True,
    )


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

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise ConnectorFetchError(f"HTTP {self.status_code}")

        def json(self) -> dict[str, object]:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):
            if "/postings/" in url and not url.endswith("/postings"):
                job_id = url.rsplit("/", 1)[-1]
                detail_ids.append(job_id)
                return _FakeResponse(_detail(job_id))
            offset = (params or {}).get("offset", 0)
            list_calls.append({"url": url, "offset": offset})
            if offset == 0:
                return _FakeResponse(
                    {
                        "limit": 100,
                        "offset": 0,
                        "totalFound": 101,
                        "content": [_summary("job-1")],
                    }
                )
            return _FakeResponse(
                {
                    "limit": 100,
                    "offset": 100,
                    "totalFound": 101,
                    "content": [_summary("job-2")],
                }
            )

    monkeypatch.setattr(
        "app.ingestion.connectors.smartrecruiters.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.smartrecruiters.asyncio.sleep", _noop_sleep)

    jobs = await SmartRecruitersConnector().fetch_jobs(_company())

    assert len(list_calls) == 2
    assert list_calls[0]["offset"] == 0
    assert list_calls[1]["offset"] == 100
    assert detail_ids == ["job-1", "job-2"]
    assert len(jobs) == 2
    assert jobs[0]["id"] == "job-1"
    assert jobs[0]["externalLink"] == "https://jobs.smartrecruiters.com/abbvie/job-1"


@pytest.mark.asyncio
async def test_zero_jobs(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"limit": 100, "offset": 0, "totalFound": 0, "content": []}

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
        "app.ingestion.connectors.smartrecruiters.httpx.AsyncClient",
        _FakeClient,
    )

    jobs = await SmartRecruitersConnector().fetch_jobs(_company())
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
            if url.endswith("/postings/missing"):
                return _FakeResponse(None, status_code=404)
            if "/postings/" in url:
                job_id = url.rsplit("/", 1)[-1]
                return _FakeResponse(_detail(job_id))
            return _FakeResponse(
                {
                    "limit": 100,
                    "offset": 0,
                    "totalFound": 2,
                    "content": [_summary("ok"), _summary("missing")],
                }
            )

    monkeypatch.setattr(
        "app.ingestion.connectors.smartrecruiters.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.smartrecruiters.asyncio.sleep", _noop_sleep)

    jobs = await SmartRecruitersConnector().fetch_jobs(_company())

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
        "app.ingestion.connectors.smartrecruiters.httpx.AsyncClient",
        _FakeClient,
    )

    with pytest.raises(ConnectorFetchError, match="SmartRecruiters fetch failed for abbvie"):
        await SmartRecruitersConnector().fetch_jobs(_company())


@pytest.mark.asyncio
async def test_malformed_list(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"totalFound": 0}

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
        "app.ingestion.connectors.smartrecruiters.httpx.AsyncClient",
        _FakeClient,
    )

    with pytest.raises(ParseError, match="Malformed SmartRecruiters list response"):
        await SmartRecruitersConnector().fetch_jobs(_company())
