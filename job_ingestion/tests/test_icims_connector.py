from __future__ import annotations

import pytest

from app.exceptions import ConnectorFetchError
from app.ingestion.connectors.icims import (
    BROWSER_IMPERSONATE,
    ICIMSConnector,
    _extract_job_id_from_url,
    _is_job_detail_url,
    _parse_detail_html,
)
from app.models.company import Company


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _icims_company() -> Company:
    return Company(
        name="SRI International",
        platform="icims",
        board_token="sri",
        platform_config={},
        is_active=True,
    )


SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://careers-sri.icims.com/jobs/6414/finance-project-analyst/job</loc>
    <lastmod>2026-06-05T16:53:18-04:00</lastmod>
  </url>
  <url>
    <loc>https://careers-sri.icims.com/jobs/6410/postdoc-formulation-science/job</loc>
    <lastmod>2026-06-11</lastmod>
  </url>
  <url>
    <loc>https://careers-sri.icims.com/jobs/search</loc>
  </url>
  <url>
    <loc>https://careers-sri.icims.com/jobs/intro</loc>
  </url>
</urlset>
"""

SRI_DETAIL_HTML = """
<html><body>
<div id="iCIMS_Header"><h1 class="iCIMS_Header">Finance Project Analyst</h1></div>
<span class="sr-only field-label">Job Locations</span>
US-CA-Menlo Park
<dl>
  <dt class="iCIMS_JobHeaderField">Category</dt>
  <dd class="iCIMS_JobHeaderData"><span>Accounting/Finance</span></dd>
  <dt class="iCIMS_JobHeaderField">Position Type</dt>
  <dd class="iCIMS_JobHeaderData"><span>Full-Time</span></dd>
</dl>
<div class="iCIMS_Expandable_Container">
  <div class="iCIMS_Expandable_Text"><p>Overview content.</p></div>
</div>
</body></html>
"""

GUIDE_DETAIL_HTML = """
<html><body>
<h1 class="iCIMS_Header">Software Engineer</h1>
<span class="iCIMS_Expandable_Label">Job Locations:</span>
<span class="iCIMS_Expandable_Field">Menlo Park, CA</span>
<span class="iCIMS_Expandable_Label">Type:</span>
<span class="iCIMS_Expandable_Field">Full-Time</span>
<span class="iCIMS_Expandable_Label">Category:</span>
<span class="iCIMS_Expandable_Field">Engineering</span>
<div class="iCIMS_Expandable_Container"><p>Guide description.</p></div>
</body></html>
"""

MINIMAL_DETAIL_HTML = """
<html><body>
<h1 class="iCIMS_Header">Title Only</h1>
<div class="iCIMS_Expandable_Container"><p>Description only.</p></div>
</body></html>
"""

MULTI_DESC_HTML = """
<html><body>
<h1 class="iCIMS_Header">Engineer</h1>
<div class="iCIMS_Expandable_Container">
  <div class="iCIMS_Expandable_Text"><p>Part one.</p></div>
</div>
<div class="iCIMS_Expandable_Container">
  <div class="iCIMS_Expandable_Text"><p>Part two.</p></div>
</div>
</body></html>
"""


def test_icims_job_id_extraction() -> None:
    assert _extract_job_id_from_url(
        "https://careers-sri.icims.com/jobs/6414/finance-project-analyst/job"
    ) == "6414"


def test_icims_sitemap_url_filter() -> None:
    assert _is_job_detail_url(
        "https://careers-sri.icims.com/jobs/6414/finance-project-analyst/job"
    )
    assert not _is_job_detail_url("https://careers-sri.icims.com/jobs/search")
    assert not _is_job_detail_url("https://careers-sri.icims.com/jobs/intro")


def test_icims_detail_parse_standard() -> None:
    parsed = _parse_detail_html(SRI_DETAIL_HTML.encode())
    assert parsed["title"] == "Finance Project Analyst"
    assert parsed["location"] == "US-CA-Menlo Park"
    assert parsed["department"] == "Accounting/Finance"
    assert parsed["employment_type_raw"] == "Full-Time"
    assert "Overview content." in parsed["raw_html"]


def test_icims_detail_parse_guide_variant() -> None:
    parsed = _parse_detail_html(GUIDE_DETAIL_HTML.encode())
    assert parsed["title"] == "Software Engineer"
    assert parsed["location"] == "Menlo Park, CA"
    assert parsed["department"] == "Engineering"
    assert parsed["employment_type_raw"] == "Full-Time"
    assert "Guide description." in parsed["raw_html"]


def test_icims_detail_missing_fields() -> None:
    parsed = _parse_detail_html(MINIMAL_DETAIL_HTML.encode())
    assert parsed["title"] == "Title Only"
    assert parsed["location"] is None
    assert parsed["department"] is None
    assert parsed["employment_type_raw"] is None
    assert "Description only." in parsed["raw_html"]


def test_icims_description_concat() -> None:
    parsed = _parse_detail_html(MULTI_DESC_HTML.encode())
    assert "Part one." in parsed["raw_html"]
    assert "Part two." in parsed["raw_html"]


@pytest.mark.asyncio
async def test_icims_sitemap_success(monkeypatch) -> None:
    class _FakeResponse:
        def __init__(self, content: bytes | str = "", status_code: int = 200, payload: dict | None = None) -> None:
            self.content = content.encode() if isinstance(content, str) else content
            self.status_code = status_code
            self._payload = payload or {}

        def json(self) -> dict:
            return self._payload

    class _FakeClient:
        def __init__(self, **kwargs: object) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str):
            if url.endswith("/sitemap.xml"):
                return _FakeResponse(SITEMAP_XML)
            if "6414" in url:
                return _FakeResponse(SRI_DETAIL_HTML)
            if "6410" in url:
                return _FakeResponse(MINIMAL_DETAIL_HTML)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.icims.asyncio.sleep", _noop_sleep)

    connector = ICIMSConnector()
    jobs = await connector.fetch_jobs(_icims_company())

    assert len(jobs) == 2
    assert {job["id"] for job in jobs} == {"6414", "6410"}
    assert jobs[0]["title"] == "Finance Project Analyst"
    assert jobs[0]["lastmod"] == "2026-06-05T16:53:18-04:00"


@pytest.mark.asyncio
async def test_icims_sitemap_405_falls_back(monkeypatch) -> None:
    listing_html = """
    <html><body>
      <a class="iCIMS_Anchor" href="/jobs/101/example-role/job">Role</a>
    </body></html>
    """

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
                return _FakeResponse(status_code=405)
            if "jobs/search" in url:
                return _FakeResponse(listing_html)
            if "101" in url:
                return _FakeResponse(MINIMAL_DETAIL_HTML)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.icims.asyncio.sleep", _noop_sleep)

    connector = ICIMSConnector()
    jobs = await connector.fetch_jobs(_icims_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "101"


@pytest.mark.asyncio
async def test_icims_sitemap_404_falls_back(monkeypatch) -> None:
    listing_html = """
    <html><body>
      <a class="iCIMS_Anchor" href="/jobs/100/example-role/job">Role</a>
    </body></html>
    """

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
            if "jobs/search" in url:
                return _FakeResponse(listing_html)
            if "100" in url:
                return _FakeResponse(MINIMAL_DETAIL_HTML)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.icims.asyncio.sleep", _noop_sleep)

    connector = ICIMSConnector()
    jobs = await connector.fetch_jobs(_icims_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "100"
    assert jobs[0]["lastmod"] is None


@pytest.mark.asyncio
async def test_icims_pagination_fallback(monkeypatch) -> None:
    page0_html = """
    <html><body>
      <a class="iCIMS_Anchor" href="/jobs/200/first-role/job">First</a>
    </body></html>
    """
    page1_html = """
    <html><body>
      <a class="iCIMS_Anchor" href="/jobs/201/second-role/job">Second</a>
    </body></html>
    """

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
            if "pr=0" in url:
                return _FakeResponse(page0_html)
            if "pr=1" in url:
                return _FakeResponse(page1_html)
            if "pr=2" in url:
                return _FakeResponse("<html><body></body></html>")
            if "200" in url or "201" in url:
                return _FakeResponse(MINIMAL_DETAIL_HTML)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.icims.asyncio.sleep", _noop_sleep)

    connector = ICIMSConnector()
    jobs = await connector.fetch_jobs(_icims_company())

    assert len(jobs) == 2
    assert {job["id"] for job in jobs} == {"200", "201"}


@pytest.mark.asyncio
async def test_icims_detail_429_retry(monkeypatch) -> None:
    calls: list[str] = []

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
            calls.append(url)
            if url.endswith("/sitemap.xml"):
                return _FakeResponse(
                    """<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                    <url><loc>https://careers-sri.icims.com/jobs/300/example/job</loc></url>
                    </urlset>"""
                )
            if "300" in url and calls.count(url) == 1:
                return _FakeResponse(status_code=429)
            if "300" in url:
                return _FakeResponse(SRI_DETAIL_HTML)
            return _FakeResponse(status_code=404)

    sleep_calls: list[float] = []

    async def _record_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.icims.asyncio.sleep", _record_sleep)

    connector = ICIMSConnector()
    jobs = await connector.fetch_jobs(_icims_company())

    assert len(jobs) == 1
    assert 5.0 in sleep_calls


@pytest.mark.asyncio
async def test_icims_detail_404_skips(monkeypatch) -> None:
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
                return _FakeResponse(SITEMAP_XML)
            if "6414" in url:
                return _FakeResponse(status_code=404)
            if "6410" in url:
                return _FakeResponse(SRI_DETAIL_HTML)
            return _FakeResponse(status_code=404)

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.icims.asyncio.sleep", _noop_sleep)

    connector = ICIMSConnector()
    jobs = await connector.fetch_jobs(_icims_company())

    assert len(jobs) == 1
    assert jobs[0]["id"] == "6410"


@pytest.mark.asyncio
async def test_icims_browser_impersonation_used(monkeypatch) -> None:
    captured_kwargs: list[dict[str, object]] = []

    class _FakeResponse:
        content = SITEMAP_XML.encode()
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

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)

    connector = ICIMSConnector()
    entries = await connector._fetch_sitemap("https://careers-sri.icims.com")

    assert len(entries) == 2
    assert captured_kwargs
    assert captured_kwargs[0]["impersonate"] == BROWSER_IMPERSONATE


@pytest.mark.asyncio
async def test_icims_detail_delay_between_calls(monkeypatch) -> None:
    sleep_calls: list[float] = []

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
                return _FakeResponse(SITEMAP_XML)
            return _FakeResponse(SRI_DETAIL_HTML)

    async def _record_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)
    monkeypatch.setattr("app.ingestion.connectors.icims.asyncio.sleep", _record_sleep)

    connector = ICIMSConnector()
    jobs = await connector.fetch_jobs(_icims_company())

    assert len(jobs) == 2
    assert sleep_calls == [2.0, 2.0]


@pytest.mark.asyncio
async def test_icims_sitemap_failure_raises(monkeypatch) -> None:
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

    monkeypatch.setattr("app.ingestion.connectors.icims.AsyncSession", _FakeClient)

    connector = ICIMSConnector()
    with pytest.raises(ConnectorFetchError, match="sitemap failed"):
        await connector._fetch_sitemap("https://careers-sri.icims.com")
