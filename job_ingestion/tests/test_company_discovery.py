from __future__ import annotations

import json
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS))

from company_discovery import (  # noqa: E402
    collect_candidates_from_urls,
    extract_ats_urls,
    extract_urls_from_search_hit,
    parse_url_to_candidate,
)


def test_extract_ats_urls_from_mixed_text() -> None:
    text = (
        "Apply at https://jobs.ashbyhq.com/acme/abc and "
        "https://job-boards.greenhouse.io/examplecorp/jobs/123"
    )
    urls = extract_ats_urls(text)
    assert "https://jobs.ashbyhq.com/acme" in urls
    assert "https://job-boards.greenhouse.io/examplecorp/jobs/123" in urls


def test_extract_urls_from_search_hit_includes_link_and_embedded_urls() -> None:
    hit = {
        "link": "https://jobs.lever.co/webfx/3c850193-9429-43fd-9afb-052adea191b3",
        "title": "Junior Engineer",
        "snippet": "Also see https://job-boards.greenhouse.io/axon/jobs/7690510003",
    }
    urls = extract_urls_from_search_hit(hit)
    assert any("jobs.lever.co/webfx" in url for url in urls)
    assert any("greenhouse.io/axon" in url for url in urls)


def test_parse_greenhouse_job_board_url() -> None:
    candidate = parse_url_to_candidate(
        "https://job-boards.greenhouse.io/pingidentity/jobs/8582872002",
        company_hint="Ping Identity",
    )
    assert candidate is not None
    assert candidate.platform == "greenhouse"
    assert candidate.board_token == "pingidentity"
    assert candidate.company == "Ping Identity"


def test_parse_ashby_application_url() -> None:
    candidate = parse_url_to_candidate(
        "https://jobs.ashbyhq.com/hadrian-automation/41472a42-c3c3-40bd-a784-8a3fbab47be3/application",
        company_hint="Hadrian",
    )
    assert candidate is not None
    assert candidate.platform == "ashby"
    assert candidate.board_token == "hadrian-automation"


def test_collect_candidates_dedupes_by_board_token() -> None:
    urls = [
        "https://jobs.lever.co/palantir/cbe90327-3e6e-451c-a54c-1d3cbcef5aeb/apply",
        "https://jobs.lever.co/palantir/d1ac83d0-e923-42a5-8e6d-58dd0cab25ca/apply",
    ]
    candidates, skipped_existing, skipped_unsupported = collect_candidates_from_urls(
        urls,
        existing_tokens=set(),
    )
    assert len(candidates) == 1
    assert candidates[0].board_token == "palantir"
    assert skipped_existing == []
    assert skipped_unsupported == []


def test_collect_candidates_skips_existing_tokens() -> None:
    urls = ["https://job-boards.greenhouse.io/axon/jobs/1"]
    candidates, skipped_existing, _ = collect_candidates_from_urls(
        urls,
        existing_tokens={"axon"},
    )
    assert candidates == []
    assert skipped_existing == ["axon"]


@pytest.mark.asyncio
async def test_validate_board_greenhouse_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    import httpx
    from company_discovery import DiscoveredCandidate, validate_board

    class FakeResponse:
        status_code = 404

        def raise_for_status(self) -> None:
            raise httpx.HTTPStatusError("not found", request=None, response=self)  # type: ignore[arg-type]

    class FakeClient:
        async def get(self, *args, **kwargs):  # noqa: ANN002, ANN003
            return FakeResponse()

    candidate = DiscoveredCandidate(
        company="Missing",
        platform="greenhouse",
        board_token="missing-board",
        source_url="https://boards.greenhouse.io/missing-board",
    )
    status, detail = await validate_board(FakeClient(), candidate)  # type: ignore[arg-type]
    assert status == "invalid"
    assert detail is not None


def test_parse_eightfold_from_url() -> None:
    from company_discovery import parse_eightfold_from_url, parse_url_to_candidate

    parsed = parse_eightfold_from_url(
        "https://explore.jobs.netflix.net/api/apply/v2/jobs?domain=netflix.com&start=0"
    )
    assert parsed is not None
    assert parsed["platform"] == "eightfold"
    assert parsed["platform_config"]["api_host"] == "explore.jobs.netflix.net"
    candidate = parse_url_to_candidate(
        "https://explore.jobs.netflix.net/api/apply/v2/jobs?domain=netflix.com&start=0"
    )
    assert candidate is not None
    assert candidate.platform == "eightfold"
    assert candidate.board_token == "netflix"


def test_parse_workday_url_to_candidate() -> None:
    from company_discovery import parse_url_to_candidate

    candidate = parse_url_to_candidate(
        "https://kbr.wd5.myworkdayjobs.com/KBR_Careers/job/Beavercreek-Ohio/Junior-Engineer_R2125329"
    )
    assert candidate is not None
    assert candidate.platform == "workday"
    assert candidate.board_token == "kbr-kbr-careers"
    assert candidate.platform_config is not None


def test_merge_candidates_dry_run(tmp_path: Path) -> None:
    from company_discovery import DiscoveredCandidate, merge_candidates_into_json

    companies_path = tmp_path / "companies.json"
    companies_path.write_text(
        json.dumps(
            [
                {
                    "company": "Existing",
                    "platform": "greenhouse",
                    "board_token": "existing",
                    "is_active": True,
                    "fetch_tier": 2,
                }
            ]
        ),
        encoding="utf-8",
    )
    candidates = [
        DiscoveredCandidate(
            company="New Co",
            platform="lever",
            board_token="newco",
            source_url="https://jobs.lever.co/newco",
            validation_status="valid",
        )
    ]
    result = merge_candidates_into_json(candidates, companies_path, dry_run=True)
    assert result["added_count"] == 1
    payload = json.loads(companies_path.read_text(encoding="utf-8"))
    assert len(payload) == 1


@pytest.mark.asyncio
async def test_fetch_cdx_page_retries_503_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    import httpx
    from company_discovery import _fetch_cdx_page

    calls = {"count": 0}

    class FakeResponse:
        def __init__(self, status_code: int, text: str = "") -> None:
            self.status_code = status_code
            self.text = text
            self.request = httpx.Request("GET", "https://index.commoncrawl.org/test-index")

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise httpx.HTTPStatusError("error", request=self.request, response=self)

    class FakeClient:
        async def get(self, *args, **kwargs):  # noqa: ANN002, ANN003
            calls["count"] += 1
            if calls["count"] == 1:
                return FakeResponse(503)
            return FakeResponse(200, '{"url": "https://boards.greenhouse.io/acme/jobs/1"}\n')

    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("company_discovery.asyncio.sleep", fake_sleep)

    urls = await _fetch_cdx_page(
        FakeClient(),  # type: ignore[arg-type]
        index_id="CC-MAIN-TEST",
        url_pattern="boards.greenhouse.io/*",
        page=0,
        page_size=10,
        max_retries=3,
        retry_base_s=2.0,
    )
    assert urls == ["https://boards.greenhouse.io/acme/jobs/1"]
    assert calls["count"] == 2
    assert sleeps == [2.0]


@pytest.mark.asyncio
async def test_fetch_cdx_page_returns_none_after_exhausted_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    import asyncio

    import httpx
    from company_discovery import _fetch_cdx_page

    class FakeResponse:
        status_code = 503
        text = ""
        request = httpx.Request("GET", "https://index.commoncrawl.org/test-index")

    class FakeClient:
        async def get(self, *args, **kwargs):  # noqa: ANN002, ANN003
            return FakeResponse()

    async def fake_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr("company_discovery.asyncio.sleep", fake_sleep)

    urls = await _fetch_cdx_page(
        FakeClient(),  # type: ignore[arg-type]
        index_id="CC-MAIN-TEST",
        url_pattern="boards.greenhouse.io/*",
        page=0,
        page_size=10,
        max_retries=2,
        retry_base_s=1.0,
    )
    assert urls is None
