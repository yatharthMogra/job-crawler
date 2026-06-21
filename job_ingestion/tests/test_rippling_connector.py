from __future__ import annotations

import json

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.rippling import RipplingConnector
from app.models.company import Company

BUILD_ID = "Pxl2Mgkh_2G068qTFlM9J"


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _summary(job_id: str, *, remote: bool = False) -> dict[str, object]:
    location: dict[str, object] = {
        "name": "Remote (United States)" if remote else "Fairfax, VA",
        "country": "United States",
        "countryCode": "US",
        "state": "Virginia" if not remote else None,
        "stateCode": "VA" if not remote else None,
        "city": "Fairfax" if not remote else None,
        "workplaceType": "REMOTE" if remote else "ON_SITE",
    }
    return {
        "id": job_id,
        "name": f"Role {job_id}",
        "url": f"https://ats.rippling.com/conceptplus/jobs/{job_id}",
        "department": {"name": "Corporate"},
        "locations": [location],
        "language": "en-US",
    }


def _detail(job_id: str) -> dict[str, object]:
    return {
        "uuid": job_id,
        "name": f"Role {job_id}",
        "url": f"https://ats.rippling.com/conceptplus/jobs/{job_id}",
        "companyName": "Concept Plus",
        "createdOn": "2026-03-23T18:05:44.354000-07:00",
        "department": {"name": "Corporate"},
        "workLocations": ["Fairfax, VA"],
        "employmentType": {"label": "SALARIED_FT", "id": "Salaried, full-time"},
        "description": {
            "company": "<p>About Concept Plus</p>",
            "role": "<p>Build systems</p>",
        },
    }


def _list_page_data(
    items: list[dict[str, object]],
    *,
    page: int = 0,
    total_items: int | None = None,
    page_size: int = 20,
) -> dict[str, object]:
    total = total_items if total_items is not None else len(items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    return {
        "items": items,
        "page": page,
        "pageSize": page_size,
        "totalItems": total,
        "totalPages": total_pages,
    }


def _list_html(*, page_data: dict[str, object]) -> str:
    next_data = {
        "props": {
            "pageProps": {
                "dehydratedState": {
                    "queries": [
                        {
                            "queryKey": [
                                "board",
                                "conceptplus",
                                "job-posts",
                                False,
                                {"page": page_data.get("page", 0)},
                            ],
                            "state": {"data": page_data},
                        }
                    ]
                }
            }
        },
        "buildId": BUILD_ID,
    }
    return (
        '<html><head></head><body>'
        f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(next_data)}</script>'
        f'"buildId":"{BUILD_ID}"'
        "</body></html>"
    )


def _list_json_payload(*, page_data: dict[str, object]) -> dict[str, object]:
    return {
        "pageProps": {
            "dehydratedState": {
                "queries": [
                    {
                        "queryKey": [
                            "board",
                            "conceptplus",
                            "job-posts",
                            False,
                            {"page": page_data.get("page", 0)},
                        ],
                        "state": {"data": page_data},
                    }
                ]
            }
        }
    }


def _detail_json_payload(job_post: dict[str, object]) -> dict[str, object]:
    return {"pageProps": {"apiData": {"jobPost": job_post}}}


def _company(*, board_token: str = "conceptplus", platform_config: dict | None = None) -> Company:
    return Company(
        name="Concept Plus",
        platform="rippling",
        board_token=board_token,
        platform_config=platform_config,
        is_active=True,
    )


@pytest.mark.asyncio
async def test_happy_path(monkeypatch) -> None:
    detail_ids: list[str] = []

    class _FakeResponse:
        def __init__(
            self,
            *,
            text: str = "",
            payload: dict[str, object] | None = None,
            status_code: int = 200,
        ) -> None:
            self.text = text
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

        async def get(self, url: str, params: dict[str, object] | None = None, headers=None):  # noqa: ANN001, ARG002
            if url.endswith("/jobs/job-1.json"):
                detail_ids.append("job-1")
                return _FakeResponse(payload=_detail_json_payload(_detail("job-1")))
            if url.endswith("/jobs.json"):
                return _FakeResponse(payload=_list_json_payload(page_data=_list_page_data([_summary("job-1")])))
            if url.endswith("/conceptplus/jobs"):
                return _FakeResponse(
                    text=_list_html(page_data=_list_page_data([_summary("job-1")])),
                )
            raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr("app.ingestion.connectors.rippling.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.rippling.asyncio.sleep", _noop_sleep)

    jobs = await RipplingConnector().fetch_jobs(_company())

    assert detail_ids == ["job-1"]
    assert len(jobs) == 1
    assert jobs[0]["id"] == "job-1"
    assert jobs[0]["externalLink"] == "https://ats.rippling.com/conceptplus/jobs/job-1"
    assert jobs[0]["description"]["role"] == "<p>Build systems</p>"


@pytest.mark.asyncio
async def test_pagination(monkeypatch) -> None:
    list_pages: list[int] = []
    detail_ids: list[str] = []

    class _FakeResponse:
        def __init__(
            self,
            *,
            text: str = "",
            payload: dict[str, object] | None = None,
            status_code: int = 200,
        ) -> None:
            self.text = text
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

        async def get(self, url: str, params: dict[str, object] | None = None, headers=None):  # noqa: ANN001, ARG002
            if "/jobs/" in url and url.endswith(".json") and not url.endswith("/jobs.json"):
                job_id = url.rsplit("/", 1)[-1].removesuffix(".json")
                detail_ids.append(job_id)
                return _FakeResponse(payload=_detail_json_payload(_detail(job_id)))
            if url.endswith("/jobs.json"):
                page = int((params or {}).get("page", 0))
                list_pages.append(page)
                if page == 0:
                    page_data = _list_page_data([_summary("job-1")], page=0, total_items=21, page_size=20)
                else:
                    page_data = _list_page_data([_summary("job-2")], page=1, total_items=21, page_size=20)
                return _FakeResponse(payload=_list_json_payload(page_data=page_data))
            if url.endswith("/conceptplus/jobs"):
                page_data = _list_page_data([_summary("job-1")], page=0, total_items=21, page_size=20)
                return _FakeResponse(text=_list_html(page_data=page_data))
            raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr("app.ingestion.connectors.rippling.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.rippling.asyncio.sleep", _noop_sleep)

    jobs = await RipplingConnector().fetch_jobs(_company())

    assert list_pages == [1]
    assert detail_ids == ["job-1", "job-2"]
    assert len(jobs) == 2


@pytest.mark.asyncio
async def test_zero_jobs(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, text: str) -> None:
            self.text = text
            self.status_code = 200

        def raise_for_status(self) -> None:
            return None

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            return _FakeResponse(text=_list_html(page_data=_list_page_data([])))

    monkeypatch.setattr("app.ingestion.connectors.rippling.httpx.AsyncClient", _FakeClient)

    jobs = await RipplingConnector().fetch_jobs(_company())
    assert jobs == []


@pytest.mark.asyncio
async def test_detail_404_skipped(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(
            self,
            *,
            text: str = "",
            payload: dict[str, object] | None = None,
            status_code: int = 200,
        ) -> None:
            self.text = text
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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            if url.endswith("/jobs/missing.json"):
                return _FakeResponse(status_code=404)
            if url.endswith("/jobs/ok.json"):
                return _FakeResponse(payload=_detail_json_payload(_detail("ok")))
            if url.endswith("/conceptplus/jobs"):
                page_data = _list_page_data([_summary("ok"), _summary("missing")])
                return _FakeResponse(text=_list_html(page_data=page_data))
            raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr("app.ingestion.connectors.rippling.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.rippling.asyncio.sleep", _noop_sleep)

    jobs = await RipplingConnector().fetch_jobs(_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "ok"


@pytest.mark.asyncio
async def test_list_http_error(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            raise RuntimeError("503 unavailable")

        @property
        def text(self) -> str:
            return ""

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.rippling.httpx.AsyncClient", _FakeClient)

    with pytest.raises(ConnectorFetchError, match="Rippling fetch failed for conceptplus"):
        await RipplingConnector().fetch_jobs(_company())


@pytest.mark.asyncio
async def test_malformed_list(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, text: str) -> None:
            self.text = text
            self.status_code = 200

        def raise_for_status(self) -> None:
            return None

    class _FakeClient:
        def __init__(self, timeout: float) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            return _FakeResponse(text="<html>no next data</html>")

    monkeypatch.setattr("app.ingestion.connectors.rippling.httpx.AsyncClient", _FakeClient)

    with pytest.raises(ParseError, match="Missing Rippling buildId"):
        await RipplingConnector().fetch_jobs(_company())


@pytest.mark.asyncio
async def test_company_slug_override(monkeypatch) -> None:
    requested_urls: list[str] = []

    class _FakeResponse:
        def __init__(self, *, text: str = "", payload: dict[str, object] | None = None) -> None:
            self.text = text
            self._payload = payload or {}
            self.status_code = 200

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

        async def get(self, url: str, params=None, headers=None):  # noqa: ANN001, ARG002
            requested_urls.append(url)
            if url.endswith("/enludio-careers/jobs"):
                page_data = _list_page_data([_summary("job-1")])
                return _FakeResponse(text=_list_html(page_data=page_data))
            if url.endswith("/jobs/job-1.json"):
                return _FakeResponse(payload=_detail_json_payload(_detail("job-1")))
            raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr("app.ingestion.connectors.rippling.httpx.AsyncClient", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.rippling.asyncio.sleep", _noop_sleep)

    company = _company(
        board_token="wrong-slug",
        platform_config={"company_slug": "enludio-careers"},
    )
    jobs = await RipplingConnector().fetch_jobs(company)

    assert any("/enludio-careers/jobs" in url for url in requested_urls)
    assert len(jobs) == 1
