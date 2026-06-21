from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.amazon_jobs import (
    AmazonJobsConnector,
    build_amazon_job_location,
    build_amazon_jobs_html,
    build_amazon_search_params,
    normalize_amazon_job,
    parse_amazon_posted_date,
    resolve_amazon_jobs_config,
    should_exclude_amazon_job,
)
from app.ingestion.job_freshness import filter_fetched_jobs
from app.models.company import Company

FIXTURES = Path(__file__).parent / "fixtures" / "amazon_jobs"


async def _noop_sleep(*_args, **_kwargs) -> None:
    return None


def _company(**platform_config: object) -> Company:
    return Company(
        name="Amazon",
        platform="amazon_jobs",
        board_token="amazon",
        platform_config=platform_config or {
            "locale": "en",
            "job_categories": ["software-development"],
            "exclude_job_categories": ["Fulfillment & Operations Management"],
            "exclude_job_families": ["Fulfillment Center"],
        },
        is_active=True,
    )


def test_parse_amazon_posted_date() -> None:
    parsed = parse_amazon_posted_date("June 19, 2026")
    assert parsed == datetime(2026, 6, 19)
    assert parse_amazon_posted_date("") is None
    assert parse_amazon_posted_date("not-a-date") is None


def test_build_amazon_search_params() -> None:
    config = resolve_amazon_jobs_config(_company(job_categories=["software-development", "data-science"]))
    params = build_amazon_search_params(config, offset=100, page_size=50)
    assert ("offset", 100) in params
    assert ("result_limit", 50) in params
    assert params.count(("category[]", "software-development")) == 1
    assert params.count(("category[]", "data-science")) == 1


def test_build_amazon_job_location_single_and_multi() -> None:
    single = {
        "normalized_location": "Seattle, Washington, USA",
        "locations": [
            '{"normalizedLocation":"Seattle, Washington, USA","location":"US, WA, Seattle"}',
        ],
    }
    assert build_amazon_job_location(single) == "Seattle, Washington, USA"

    multi = {
        "normalized_location": "Austin, Texas, USA",
        "locations": [
            '{"normalizedLocation":"Austin, Texas, USA","location":"US, TX, Austin"}',
            '{"normalizedLocation":"Seattle, Washington, USA","location":"US, WA, Seattle"}',
        ],
    }
    location = build_amazon_job_location(multi)
    assert "Austin, Texas, USA" in location
    assert "Seattle, Washington, USA" in location


def test_should_exclude_amazon_job() -> None:
    config = resolve_amazon_jobs_config(_company())
    assert should_exclude_amazon_job(
        {
            "job_category": "Fulfillment & Operations Management",
            "job_family": "Operations",
        },
        config,
    )
    assert not should_exclude_amazon_job(
        {
            "job_category": "Software Development",
            "job_family": "Software Development",
        },
        config,
    )


def test_build_amazon_jobs_html() -> None:
    html = build_amazon_jobs_html(
        {
            "business_category": "aws",
            "job_category": "Software Development",
            "job_family": "Software Development",
            "description": "Build services.",
            "basic_qualifications": "3+ years experience",
            "preferred_qualifications": "AWS experience",
        }
    )
    assert "Description" in html
    assert "Basic Qualifications" in html
    assert "Preferred Qualifications" in html
    assert "Build services." in html


def test_normalize_amazon_job() -> None:
    normalized = normalize_amazon_job(
        {
            "id_icims": "10454425",
            "job_path": "/en/jobs/10454425/sde-ii-amazon-india-ads",
            "title": "SDE II",
            "description": "Build ads.",
        }
    )
    assert normalized["id"] == "10454425"
    assert normalized["externalLink"] == (
        "https://www.amazon.jobs/en/jobs/10454425/sde-ii-amazon-india-ads"
    )
    assert "Build ads." in normalized["raw_html"]


def test_parse_list_fixture_excludes_fulfillment() -> None:
    payload = json.loads((FIXTURES / "search_page.json").read_text())
    config = resolve_amazon_jobs_config(_company())
    kept = [
        job
        for job in payload["jobs"]
        if isinstance(job, dict) and not should_exclude_amazon_job(job, config)
    ]
    assert any(job.get("job_category") == "Software Development" for job in kept)
    assert all(job.get("id_icims") != "99999999" for job in kept)


@pytest.mark.asyncio
async def test_pagination_and_category_params(monkeypatch) -> None:
    page_one = json.loads((FIXTURES / "search_page.json").read_text())
    page_two = {"hits": page_one["hits"], "jobs": []}
    calls: list[tuple[str, list[tuple[str, str | int]]]] = []

    class _FakeResponse:
        def __init__(self, payload: dict) -> None:
            self._payload = payload

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float, headers: dict[str, str] | None = None) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: list[tuple[str, str | int]] | None = None):
            calls.append((url, list(params or [])))
            offset = next((value for key, value in (params or []) if key == "offset"), 0)
            if offset == 0:
                return _FakeResponse(page_one)
            return _FakeResponse(page_two)

    monkeypatch.setattr(
        "app.ingestion.connectors.amazon_jobs.httpx.AsyncClient",
        _FakeClient,
    )
    monkeypatch.setattr("app.ingestion.connectors.amazon_jobs.asyncio.sleep", _noop_sleep)

    monkeypatch.setattr(AmazonJobsConnector, "page_size", 2)
    jobs = await AmazonJobsConnector().fetch_jobs(_company())

    assert calls[0][0] == "https://www.amazon.jobs/en/search.json"
    assert ("category[]", "software-development") in calls[0][1]
    assert len(calls) == 2
    assert len(jobs) == 3
    assert all(job["id"] for job in jobs)
    assert jobs[0]["externalLink"].startswith("https://www.amazon.jobs/en/jobs/")


@pytest.mark.asyncio
async def test_malformed_response_raises_parse_error(monkeypatch) -> None:
    class _FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"hits": 0}

    class _FakeClient:
        def __init__(self, timeout: float, headers: dict[str, str] | None = None) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: list[tuple[str, str | int]] | None = None):
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.amazon_jobs.httpx.AsyncClient",
        _FakeClient,
    )

    with pytest.raises(ParseError):
        await AmazonJobsConnector().fetch_jobs(_company())


@pytest.mark.asyncio
async def test_http_failure_raises_connector_fetch_error(monkeypatch) -> None:
    class _FakeClient:
        def __init__(self, timeout: float, headers: dict[str, str] | None = None) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, url: str, params: list[tuple[str, str | int]] | None = None):
            raise RuntimeError("network down")

    monkeypatch.setattr(
        "app.ingestion.connectors.amazon_jobs.httpx.AsyncClient",
        _FakeClient,
    )

    with pytest.raises(ConnectorFetchError):
        await AmazonJobsConnector().fetch_jobs(_company())


def test_filter_fetched_jobs_respects_posted_date() -> None:
    fresh = normalize_amazon_job(
        {
            "id_icims": "100",
            "job_path": "/en/jobs/100/fresh",
            "posted_date": "June 20, 2026",
            "description": "Fresh role",
        }
    )
    stale = normalize_amazon_job(
        {
            "id_icims": "101",
            "job_path": "/en/jobs/101/stale",
            "posted_date": "May 1, 2026",
            "description": "Stale role",
        }
    )
    reference = datetime(2026, 6, 20, tzinfo=timezone.utc)
    kept, rejected = filter_fetched_jobs(
        [fresh, stale],
        "amazon_jobs",
        reference=reference,
        max_age_days=7,
    )
    assert len(kept) == 1
    assert kept[0]["id"] == "100"
    assert rejected == 1
