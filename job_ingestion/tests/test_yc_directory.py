from __future__ import annotations

import pytest

from app.ingestion.connectors.yc_directory import (
    derive_career_urls,
    detect_ats_from_html,
    fetch_all_yc_companies,
)


def test_derive_career_urls() -> None:
    urls = derive_career_urls("https://example.com/about")
    assert urls[0] == "https://example.com/careers"
    assert urls[-1] == "https://example.com"


def test_detect_ats_from_html_greenhouse() -> None:
    html = '<a href="https://boards.greenhouse.io/acme/jobs/1">Apply</a>'
    ats, token, workday = detect_ats_from_html(html)
    assert ats == "greenhouse"
    assert token == "acme"
    assert workday is None


def test_detect_ats_from_html_workday() -> None:
    html = "https://acme.wd5.myworkdayjobs.com/en-US/careers"
    ats, token, workday = detect_ats_from_html(html)
    assert ats == "workday"
    assert token == "acme"
    assert workday is not None
    assert workday.instance == "wd5"


@pytest.mark.asyncio
async def test_fetch_all_yc_companies_pagination(monkeypatch) -> None:
    pages = [
        [{"id": 1, "name": "A", "hiring": True}],
        [],
    ]

    class _FakeResponse:
        def __init__(self, payload):
            self._payload = payload

        def raise_for_status(self) -> None:
            return None

        def json(self):
            return self._payload

    class _FakeClient:
        async def get(self, url: str, params=None):  # noqa: ARG002
            page = params.get("page", 1)
            return _FakeResponse(pages[page - 1] if page - 1 < len(pages) else [])

    monkeypatch.setattr("app.ingestion.connectors.yc_directory.asyncio.sleep", lambda *_a, **_k: None)
    companies = await fetch_all_yc_companies(_FakeClient())
    assert len(companies) == 1
    assert companies[0]["name"] == "A"
