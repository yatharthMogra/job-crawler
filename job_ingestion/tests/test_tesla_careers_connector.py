from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.tesla_careers import (
    TeslaCareersConnector,
    build_tesla_careers_html,
    build_tesla_job_url,
    build_tesla_jobs_from_push,
    extract_job_id_from_url,
    filter_listings_by_site,
    get_location_ids_in_country,
    normalize_tesla_job,
    pending_tesla_detail_ids,
    resolve_tesla_careers_config,
)
from app.ingestion.extractor.deterministic import extract_deterministic_fields
from app.models.company import Company

FIXTURES = Path(__file__).parent / "fixtures" / "tesla_careers"


def _company(**platform_config: object) -> Company:
    return Company(
        name="Tesla",
        platform="tesla_careers",
        board_token="tesla",
        platform_config=platform_config or {"sites": ["US"]},
        is_active=True,
    )


def _state() -> dict:
    return json.loads((FIXTURES / "state.json").read_text())


def _detail(job_id: str = "224501") -> dict:
    detail = json.loads((FIXTURES / "detail_224501.json").read_text())
    if job_id != "224501":
        return {**detail, "id": job_id, "title": f"Job {job_id}"}
    return detail


def test_extract_job_id_from_url() -> None:
    assert (
        extract_job_id_from_url(
            "https://www.tesla.com/careers/search/job/ai-engineer-manipulation-optimus-224501"
        )
        == "224501"
    )
    assert extract_job_id_from_url("https://www.tesla.com/careers/search/") is None


def test_build_tesla_job_url() -> None:
    assert (
        build_tesla_job_url("/careers/search/job/ai-engineer-manipulation-optimus-224501")
        == "https://www.tesla.com/careers/search/job/ai-engineer-manipulation-optimus-224501"
    )


def test_resolve_tesla_careers_config_defaults_to_us() -> None:
    config = resolve_tesla_careers_config(_company())
    assert config["sites"] == ["US"]
    assert config["ingestion_mode"] is None
    assert config["expected_push_interval_hours"] == 4

    config = resolve_tesla_careers_config(
        _company(sites=["US", "DE"], ingestion_mode="manual_push", expected_push_interval_hours=6)
    )
    assert config["sites"] == ["US", "DE"]
    assert config["ingestion_mode"] == "manual_push"
    assert config["expected_push_interval_hours"] == 6


def test_get_location_ids_in_country() -> None:
    state = _state()
    us_site = state["geo"][0]["sites"][0]
    location_ids = get_location_ids_in_country(us_site)
    assert "401022" in location_ids
    assert "10759" in location_ids


def test_filter_listings_by_site() -> None:
    state = _state()
    us_jobs = filter_listings_by_site(state, "US")
    assert len(us_jobs) == 2
    assert {job["id"] for job in us_jobs} == {"224501", "221945"}

    de_jobs = filter_listings_by_site(state, "DE")
    assert len(de_jobs) == 1
    assert de_jobs[0]["id"] == "999999"


def test_pending_tesla_detail_ids() -> None:
    state = _state()
    pending = pending_tesla_detail_ids(state, ["US"], known_external_ids={"224501"})
    assert pending == ["221945"]


def test_build_tesla_jobs_from_push_new_and_cached() -> None:
    state = _state()
    cached = normalize_tesla_job(
        state["listings"][0],
        _detail("224501"),
        site="US",
        lookup=state["lookup"],
    )
    jobs = build_tesla_jobs_from_push(
        state,
        {"221945": _detail("221945")},
        sites=["US"],
        previous_raw_by_id={"224501": cached},
    )
    assert {job["id"] for job in jobs} == {"224501", "221945"}
    assert jobs[0]["id"] == "224501"
    assert "humanoid robots" in next(job for job in jobs if job["id"] == "224501")["raw_html"]


def test_build_tesla_jobs_from_push_missing_detail_raises() -> None:
    state = _state()
    with pytest.raises(ParseError, match="detail payload is missing"):
        build_tesla_jobs_from_push(state, {}, sites=["US"], previous_raw_by_id={})


def test_build_tesla_careers_html() -> None:
    detail = _detail()
    html = build_tesla_careers_html(detail)
    assert "What to Expect" in html
    assert "humanoid robots" in html
    assert "What You'll Do" in html


def test_normalize_tesla_job() -> None:
    state = _state()
    listing = state["listings"][0]
    detail = _detail()
    normalized = normalize_tesla_job(
        listing,
        detail,
        site="US",
        lookup=state["lookup"],
    )
    assert normalized["id"] == "224501"
    assert normalized["title"] == "AI Engineer, Manipulation, Optimus"
    assert normalized["location"] == "Palo Alto, California"
    assert normalized["department"] == "Tesla AI"
    assert normalized["site"] == "US"
    assert normalized["externalLink"].endswith("ai-engineer-manipulation-optimus-224501")
    assert "humanoid robots" in normalized["raw_html"]


def test_extract_deterministic_fields() -> None:
    detail = _detail()
    job = normalize_tesla_job(
        {"id": "224501", "t": detail["title"], "l": "401022", "dp": "5", "y": 1},
        detail,
        site="US",
    )
    fields = extract_deterministic_fields(job, platform="tesla_careers")
    assert fields["external_job_id"] == "224501"
    assert fields["title"] == "AI Engineer, Manipulation, Optimus"
    assert fields["location"] == "Palo Alto, California"
    assert fields["department"] == "Tesla AI"
    assert fields["employment_type"] == "Full-time"
    assert "humanoid robots" in fields["raw_html"]


@pytest.mark.asyncio
async def test_fetch_jobs_is_push_only() -> None:
    connector = TeslaCareersConnector()
    with pytest.raises(ConnectorFetchError, match="push-only"):
        await connector.fetch_jobs(_company())


def test_filter_listings_by_site_missing_geo_raises() -> None:
    with pytest.raises(ParseError):
        filter_listings_by_site({"listings": []}, "US")
