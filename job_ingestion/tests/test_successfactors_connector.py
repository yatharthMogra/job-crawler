from __future__ import annotations

from pathlib import Path

import pytest

from app.exceptions import ConnectorFetchError
from app.ingestion.connectors.successfactors import (
    BROWSER_IMPERSONATE,
    SuccessFactorsConnector,
    extract_job_id_from_url,
    is_job_detail_url,
    parse_successfactors_date_posted,
    parse_successfactors_detail_html,
)
from app.models.company import Company

FIXTURES = Path(__file__).parent / "fixtures" / "successfactors"


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _mcdonalds_company() -> Company:
    return Company(
        name="McDonald's",
        platform="successfactors",
        board_token="mcdonalds",
        platform_config={
            "career_site_url": "https://jobs.mcdonalds.com",
            "locale": "en_US",
            "search_page_size": 10,
        },
        is_active=True,
    )


def _westinghouse_company() -> Company:
    return Company(
        name="Westinghouse Electric Company",
        platform="successfactors",
        board_token="westinghouse-nuclear",
        platform_config={
            "career_site_url": "https://careers.westinghousenuclear.com",
            "locale": "en_US",
            "search_page_size": 25,
            "search_default_params": {"searchby": "location", "d": "10"},
        },
        is_active=True,
    )


def test_job_id_extraction() -> None:
    assert (
        extract_job_id_from_url(
            "https://jobs.mcdonalds.com/job/Chicago-Software-Engineer-I-iOS-IL-60607/1322170500/"
        )
        == "1322170500"
    )


def test_job_url_filter() -> None:
    assert is_job_detail_url(
        "https://jobs.mcdonalds.com/job/Chicago-Software-Engineer-I-iOS-IL-60607/1322170500/"
    )
    assert not is_job_detail_url("https://jobs.mcdonalds.com/search/")


def test_parse_mcdonalds_detail_fixture() -> None:
    html = (FIXTURES / "mcdonalds_detail.html").read_text()
    parsed = parse_successfactors_detail_html(html)
    assert parsed["title"] == "Software Engineer I - iOS"
    assert parsed["location"] == "Chicago, IL, US, 60607"
    assert parsed["datePosted"] == "Sat Jun 20 07:00:00 UTC 2026"
    assert "Build mobile apps." in parsed["raw_html"]


def test_parse_westinghouse_detail_fixture() -> None:
    html = (FIXTURES / "westinghouse_detail.html").read_text()
    parsed = parse_successfactors_detail_html(html)
    assert parsed["title"] == "Senior Data Engineer"
    assert parsed["location"] == "Cranberry Township, US"
    assert parsed["datePosted"] == "Sat Jun 20 07:00:00 UTC 2026"
    assert "Data platform work." in parsed["raw_html"]


def test_parse_date_posted_formats() -> None:
    posted = parse_successfactors_date_posted("Sat Jun 20 07:00:00 UTC 2026")
    assert posted is not None
    assert posted.year == 2026
    assert posted.month == 6
    assert posted.day == 20

    lastmod = parse_successfactors_date_posted("2026-06-13")
    assert lastmod is not None
    assert lastmod.year == 2026


@pytest.mark.asyncio
async def test_sitemap_success_mcdonalds(monkeypatch) -> None:
    sitemap = (FIXTURES / "mcdonalds_sitemap.xml").read_text()
    detail = (FIXTURES / "mcdonalds_detail.html").read_text()

    class _FakeResponse:
        def __init__(self, content: bytes | str = "", status_code: int = 200) -> None:
            self.content = content.encode() if isinstance(content, str) else content
            self.status_code = status_code

    class _FakeClient:
        def __init__(self, **kwargs: object) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str):
            if url.endswith("/sitemap.xml"):
                return _FakeResponse(sitemap)
            if "1322170500" in url:
                return _FakeResponse(detail)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.successfactors.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.successfactors.asyncio.sleep", _noop_sleep)

    connector = SuccessFactorsConnector()
    jobs = await connector.fetch_jobs(_mcdonalds_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "1322170500"
    assert jobs[0]["title"] == "Software Engineer I - iOS"
    assert jobs[0]["lastmod"] == "2026-06-13"
    assert jobs[0]["externalLink"].endswith("/1322170500/")


@pytest.mark.asyncio
async def test_sitemap_success_westinghouse(monkeypatch) -> None:
    sitemap = (FIXTURES / "westinghouse_sitemap.xml").read_text()
    detail = (FIXTURES / "westinghouse_detail.html").read_text()

    class _FakeResponse:
        def __init__(self, content: bytes | str = "", status_code: int = 200) -> None:
            self.content = content.encode() if isinstance(content, str) else content
            self.status_code = status_code

    class _FakeClient:
        def __init__(self, **kwargs: object) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str):
            if url.endswith("/sitemap.xml"):
                return _FakeResponse(sitemap)
            if "1385011200" in url:
                return _FakeResponse(detail)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.successfactors.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.successfactors.asyncio.sleep", _noop_sleep)

    connector = SuccessFactorsConnector()
    jobs = await connector.fetch_jobs(_westinghouse_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "1385011200"
    assert jobs[0]["title"] == "Senior Data Engineer"


@pytest.mark.asyncio
async def test_sitemap_404_falls_back_to_search_pagination(monkeypatch) -> None:
    search_page = (FIXTURES / "mcdonalds_search_page.html").read_text()
    detail = (FIXTURES / "mcdonalds_detail.html").read_text()

    class _FakeResponse:
        def __init__(self, content: bytes | str = "", status_code: int = 200) -> None:
            self.content = content.encode() if isinstance(content, str) else content
            self.status_code = status_code

    class _FakeClient:
        def __init__(self, **kwargs: object) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str):
            if url.endswith("/sitemap.xml"):
                return _FakeResponse(status_code=404)
            if "/search/" in url:
                return _FakeResponse(search_page)
            if "1322170500" in url or "1388992000" in url:
                return _FakeResponse(detail)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.successfactors.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.successfactors.asyncio.sleep", _noop_sleep)

    connector = SuccessFactorsConnector()
    jobs = await connector.fetch_jobs(_mcdonalds_company())

    assert len(jobs) == 2
    assert {job["id"] for job in jobs} == {"1322170500", "1388992000"}


@pytest.mark.asyncio
async def test_detail_404_skips(monkeypatch) -> None:
    sitemap = (FIXTURES / "mcdonalds_sitemap.xml").read_text()
    detail = (FIXTURES / "mcdonalds_detail.html").read_text()

    class _FakeResponse:
        def __init__(self, content: bytes | str = "", status_code: int = 200) -> None:
            self.content = content.encode() if isinstance(content, str) else content
            self.status_code = status_code

    class _FakeClient:
        def __init__(self, **kwargs: object) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str):
            if url.endswith("/sitemap.xml"):
                return _FakeResponse(sitemap)
            if "1322170500" in url:
                return _FakeResponse(status_code=404)
            if "1388992000" in url:
                return _FakeResponse(detail)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.successfactors.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.successfactors.asyncio.sleep", _noop_sleep)

    connector = SuccessFactorsConnector()
    jobs = await connector.fetch_jobs(_mcdonalds_company())

    assert len(jobs) == 0


@pytest.mark.asyncio
async def test_browser_impersonation_used(monkeypatch) -> None:
    captured_kwargs: list[dict[str, object]] = []
    sitemap = (FIXTURES / "mcdonalds_sitemap.xml").read_text()

    class _FakeResponse:
        content = sitemap.encode()
        status_code = 200

    class _FakeClient:
        def __init__(self, **kwargs: object) -> None:
            captured_kwargs.append(kwargs)

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.successfactors.AsyncSession", _FakeClient)

    connector = SuccessFactorsConnector()
    entries = await connector._fetch_job_entries(
        _mcdonalds_company(), "https://jobs.mcdonalds.com"
    )

    assert len(entries) == 1
    assert captured_kwargs
    assert captured_kwargs[0]["impersonate"] == BROWSER_IMPERSONATE


@pytest.mark.asyncio
async def test_sitemap_failure_raises(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 500
        content = b""

    class _FakeClient:
        def __init__(self, **kwargs: object) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr("app.ingestion.connectors.successfactors.AsyncSession", _FakeClient)

    connector = SuccessFactorsConnector()
    with pytest.raises(ConnectorFetchError, match="sitemap failed"):
        await connector._fetch_job_entries(_mcdonalds_company(), "https://jobs.mcdonalds.com")
