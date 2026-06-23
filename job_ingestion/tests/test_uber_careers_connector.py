from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.exceptions import ParseError
from app.ingestion.connectors.uber_careers import (
    UberCareersConnector,
    build_uber_careers_html,
    build_uber_job_location,
    build_uber_job_url,
    build_uber_search_body,
    normalize_uber_job,
    parse_uber_total_results,
    resolve_uber_careers_config,
)
from app.ingestion.extractor.deterministic import extract_deterministic_fields
from app.models.company import Company

FIXTURES = Path(__file__).parent / "fixtures" / "uber_careers"


def _company(**platform_config: object) -> Company:
    return Company(
        name="Uber",
        platform="uber_careers",
        board_token="uber",
        platform_config=platform_config or {"locale_path": "us/en"},
        is_active=True,
    )


def test_parse_uber_total_results() -> None:
    assert parse_uber_total_results({"low": 922, "high": 0, "unsigned": False}) == 922
    assert parse_uber_total_results(100) == 100
    assert parse_uber_total_results(None) is None


def test_build_uber_search_body() -> None:
    config = resolve_uber_careers_config(_company())
    body = build_uber_search_body(
        limit=50,
        offset=100,
        params=config["search_params"],
    )
    assert body["limit"] == 50
    assert body["offset"] == 100
    assert body["params"]["query"] == ""


def test_build_uber_job_location_single_and_multi() -> None:
    single = {
        "location": {
            "city": "Amsterdam",
            "region": None,
            "countryName": "Netherlands",
        },
        "allLocations": [
            {"city": "Amsterdam", "region": None, "countryName": "Netherlands"},
        ],
    }
    assert build_uber_job_location(single) == "Amsterdam, Netherlands"

    multi = {
        "location": {"city": "Chicago", "region": "Illinois", "countryName": "United States"},
        "allLocations": [
            {"city": "Chicago", "region": "Illinois", "countryName": "United States"},
            {"city": "New York", "region": "New York", "countryName": "United States"},
            {"city": "Sao Paulo", "region": "São Paulo", "countryName": "Brazil"},
        ],
    }
    location = build_uber_job_location(multi)
    assert "Chicago, Illinois, United States" in location
    assert "New York, New York, United States" in location
    assert "Sao Paulo, São Paulo, Brazil" in location


def test_build_uber_job_url() -> None:
    assert build_uber_job_url(157470, "us/en") == (
        "https://www.uber.com/us/en/careers/list/157470/"
    )


def test_build_uber_careers_html() -> None:
    html = build_uber_careers_html(
        {
            "department": "Engineering",
            "team": "Platform",
            "timeType": "Full-Time",
            "description": "About the role\n\nBuild systems.",
        }
    )
    assert "Department" in html
    assert "Engineering" in html
    assert "Build systems." in html


def test_normalize_uber_job_from_fixture() -> None:
    payload = json.loads((FIXTURES / "search_response_page.json").read_text())
    raw = payload["data"]["results"][0]
    normalized = normalize_uber_job(raw, locale_path="us/en")

    assert normalized["id"] == str(raw["id"])
    assert normalized["title"] == raw["title"]
    assert "Netherlands" in normalized["location"]
    assert normalized["externalLink"].endswith(f"/careers/list/{raw['id']}/")
    assert normalized["raw_html"]


def test_extract_deterministic_fields() -> None:
    payload = json.loads((FIXTURES / "search_response_page.json").read_text())
    job = normalize_uber_job(payload["data"]["results"][0], locale_path="us/en")
    fields = extract_deterministic_fields(job, platform="uber_careers")

    assert fields["external_job_id"] == job["id"]
    assert fields["title"] == job["title"]
    assert fields["location"] == job["location"]
    assert fields["posting_url"] == job["externalLink"]
    assert fields["posted_at"] is not None
    assert fields["employment_type"] == "Full-Time"


@pytest.mark.asyncio
async def test_probe_then_full_fetch(monkeypatch) -> None:
    page_one = json.loads((FIXTURES / "search_response_page.json").read_text())
    full_payload = {
        "status": "success",
        "data": {
            "results": page_one["data"]["results"]
            + [
                {
                    "id": 999001,
                    "title": "Second Batch Role",
                    "description": "More work.",
                    "department": "Engineering",
                    "team": "Core",
                    "timeType": "Full-Time",
                    "location": {
                        "city": "London",
                        "region": None,
                        "countryName": "United Kingdom",
                    },
                    "allLocations": [
                        {
                            "city": "London",
                            "region": None,
                            "countryName": "United Kingdom",
                        }
                    ],
                    "creationDate": "2026-01-01T00:00:00.000Z",
                    "updatedDate": "2026-01-02T00:00:00.000Z",
                }
            ],
            "totalResults": page_one["data"]["totalResults"],
        },
    }
    calls: list[int] = []

    class _FakeResponse:
        def __init__(self, payload: dict, status_code: int = 200) -> None:
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP {self.status_code}")

        def json(self) -> dict:
            return self._payload

    class _FakeClient:
        def __init__(self, timeout: float, headers: dict[str, str] | None = None, follow_redirects: bool = True) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict):  # noqa: A002
            calls.append(json["limit"])
            if json["limit"] == 50:
                return _FakeResponse(page_one)
            return _FakeResponse(full_payload)

        async def get(self, url: str, headers: dict[str, str] | None = None):  # noqa: ARG002
            return _FakeResponse({})

    monkeypatch.setattr(
        "app.ingestion.connectors.uber_careers.httpx.AsyncClient",
        _FakeClient,
    )

    jobs = await UberCareersConnector().fetch_jobs(_company())

    assert calls == [50, 922]
    assert len(jobs) == 4
    assert jobs[-1]["id"] == "999001"


@pytest.mark.asyncio
async def test_malformed_response_raises_parse_error(monkeypatch) -> None:
    class _FakeResponse:
        status_code = 200

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"status": "error"}

    class _FakeClient:
        def __init__(self, timeout: float, headers: dict[str, str] | None = None, follow_redirects: bool = True) -> None:  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def post(self, url: str, json: dict):  # noqa: A002
            return _FakeResponse()

        async def get(self, url: str, headers: dict[str, str] | None = None):  # noqa: ARG002
            return _FakeResponse()

    monkeypatch.setattr(
        "app.ingestion.connectors.uber_careers.httpx.AsyncClient",
        _FakeClient,
    )

    with pytest.raises(ParseError):
        await UberCareersConnector().fetch_jobs(_company())
