from __future__ import annotations

from pathlib import Path

import pytest

from app.exceptions import ConnectorFetchError
from app.ingestion.connectors.google_careers import (
    GoogleCareersConnector,
    extract_job_id_from_url,
    parse_google_careers_detail_html,
    parse_google_careers_list_page,
)
from app.models.company import Company

FIXTURES = Path(__file__).parent / "fixtures" / "google_careers"


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _company() -> Company:
    return Company(
        name="Google",
        platform="google_careers",
        board_token="google",
        is_active=True,
    )


def test_extract_job_id_from_url() -> None:
    assert (
        extract_job_id_from_url(
            "jobs/results/143122286080074438-forward-deployed-engineer-iv-genai-google-cloud"
        )
        == "143122286080074438"
    )
    assert extract_job_id_from_url("https://www.google.com/about/careers/applications/jobs/results/101350183731634886-product-manager-google-fonts") == "101350183731634886"


def test_parse_list_page_fixture() -> None:
    html = (FIXTURES / "list_page.html").read_text()
    summaries, total = parse_google_careers_list_page(html)

    assert total == 3626
    assert len(summaries) == 20

    multi_loc = next(item for item in summaries if item["id"] == "143122286080074438")
    assert multi_loc["title"] == "Forward Deployed Engineer IV, GenAI, Google Cloud"
    assert multi_loc["organization"] == "Google"
    assert "San Francisco, CA, USA" in multi_loc["location"]
    assert "+24 more" in multi_loc["location"]
    assert multi_loc["experience_level"] == "Advanced"
    assert multi_loc["externalLink"].endswith(
        "143122286080074438-forward-deployed-engineer-iv-genai-google-cloud"
    )
    assert "RAG-like" in multi_loc["list_min_qualifications"]

    deepmind = next(item for item in summaries if item["id"] == "132507027548054214")
    assert deepmind["organization"] == "DeepMind"


def test_parse_detail_page_fixture() -> None:
    html = (FIXTURES / "detail_page.html").read_text()
    parsed = parse_google_careers_detail_html(html, experience_level="Advanced")

    assert "Experience level:</strong> Advanced" in parsed["raw_html"]
    assert "About the job" in parsed["raw_html"]
    assert "Responsibilities" in parsed["raw_html"]
    assert "Minimum qualifications" in parsed["raw_html"]
    assert "Preferred qualifications" in parsed["raw_html"]
    assert "RAG-like architectures" in parsed["raw_html"]


@pytest.mark.asyncio
async def test_pagination_and_detail_fetch(monkeypatch) -> None:
    list_html = (FIXTURES / "list_page.html").read_text()
    detail_html = (FIXTURES / "detail_page.html").read_text()
    list_calls: list[int] = []
    detail_urls: list[str] = []

    class _FakeResponse:
        def __init__(self, text: str = "", status_code: int = 200) -> None:
            self.text = text
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise ConnectorFetchError(f"HTTP {self.status_code}")

    class _FakeClient:
        def __init__(self, timeout: float, headers: dict[str, str] | None = None) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):
            if "/jobs/results/" in url and url.rstrip("/").split("/")[-1] != "results":
                detail_urls.append(url)
                return _FakeResponse(detail_html)
            page = int((params or {}).get("page", 1))
            list_calls.append(page)
            return _FakeResponse(list_html)

    monkeypatch.setattr(
        "app.ingestion.connectors.google_careers.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.google_careers.asyncio.sleep", _noop_sleep)

    jobs = await GoogleCareersConnector().fetch_jobs(_company())

    assert list_calls == [1, 2]
    assert len(detail_urls) == 20
    assert len(jobs) == 20
    assert jobs[0]["id"]
    assert jobs[0]["raw_html"]
    assert jobs[0]["externalLink"].startswith("https://www.google.com/about/careers/applications/")


@pytest.mark.asyncio
async def test_detail_404_skipped(monkeypatch) -> None:
    list_html = (FIXTURES / "list_page.html").read_text()

    class _FakeResponse:
        def __init__(self, text: str = "", status_code: int = 200) -> None:
            self.text = text
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise ConnectorFetchError(f"HTTP {self.status_code}")

    class _FakeClient:
        def __init__(self, timeout: float, headers: dict[str, str] | None = None) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: dict[str, object] | None = None):
            if "/jobs/results/" in url and url.rstrip("/").split("/")[-1] != "results":
                return _FakeResponse(status_code=404)
            return _FakeResponse(list_html)

    monkeypatch.setattr(
        "app.ingestion.connectors.google_careers.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.google_careers.asyncio.sleep", _noop_sleep)

    jobs = await GoogleCareersConnector().fetch_jobs(_company())
    assert jobs == []
