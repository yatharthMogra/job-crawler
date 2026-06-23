#!/usr/bin/env python3
"""Live smoke test for newly added company connectors (limited scope)."""
from __future__ import annotations

import asyncio
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ingestion.connectors.apple_careers import AppleCareersConnector
from app.ingestion.connectors.eightfold import EightfoldConnector
from app.ingestion.connectors.oracle_hcm import OracleHCMConnector
from app.ingestion.connectors.talentbrew import TalentBrewConnector
from app.ingestion.connectors.workday import WorkdayConnector
from app.ingestion.fetcher import get_connector
from app.models.company import Company


@dataclass
class SmokeCase:
    label: str
    company: Company
    detail_limit: int = 3


def _company(
    name: str,
    platform: str,
    board_token: str,
    platform_config: dict[str, Any],
) -> Company:
    return Company(
        name=name,
        platform=platform,
        board_token=board_token,
        platform_config=platform_config,
        is_active=True,
        fetch_tier=2,
    )


SMOKE_CASES = [
    SmokeCase(
        "Cisco (workday)",
        _company(
            "Cisco",
            "workday",
            "cisco",
            {
                "tenant": "cisco",
                "instance": "wd5",
                "career_site": "Cisco_Careers",
                "public_path_prefix": "Cisco_Careers",
            },
        ),
    ),
    SmokeCase(
        "BlackRock (talentbrew)",
        _company(
            "BlackRock",
            "talentbrew",
            "blackrock",
            {
                "base_url": "https://careers.blackrock.com",
                "company_id": "45831",
            },
        ),
    ),
    SmokeCase(
        "Goldman Sachs (oracle_hcm)",
        _company(
            "Goldman Sachs",
            "oracle_hcm",
            "hdpc",
            {
                "datacenter": "us2",
                "site_number": "LateralHiring",
                "public_url_base": "https://higher.gs.com/roles",
            },
        ),
    ),
    SmokeCase(
        "Apple (apple_careers)",
        _company(
            "Apple",
            "apple_careers",
            "apple",
            {
                "locale": "en-us",
                "location": "united-states-USA",
                "teams": ["apps-and-frameworks-SFTWR-AF"],
            },
        ),
    ),
    SmokeCase(
        "Millennium experienced (eightfold)",
        _company(
            "Millennium Management",
            "eightfold",
            "millennium-experienced",
            {"api_host": "career.mlp.com", "domain": "mlp.com"},
        ),
    ),
    SmokeCase(
        "Millennium campus (eightfold)",
        _company(
            "Millennium Management (Campus)",
            "eightfold",
            "millennium-campus",
            {
                "api_host": "campusjobs.mlp.com",
                "domain": "mlp.com",
                "extra_params": {"microsite": "campus-site"},
            },
        ),
    ),
]


def _sample_from_job(job: dict[str, Any]) -> dict[str, Any]:
    title = job.get("title") or job.get("Title") or job.get("name") or job.get("jobOpeningName")
    job_id = job.get("id") or job.get("Id")
    link = job.get("externalLink")
    raw_html = (
        job.get("raw_html")
        or job.get("job_description")
        or job.get("ExternalDescriptionStr")
        or job.get("jobDescription")
        or ""
    )
    if isinstance(raw_html, dict):
        raw_html = str(raw_html)
    return {
        "id": job_id,
        "title": title,
        "url": link,
        "description_chars": len(str(raw_html)),
    }


async def _limited_workday_fetch(connector: WorkdayConnector, company: Company, limit: int) -> list[dict]:
    import httpx

    base_url = connector._base_url(company)
    public_base_url = connector._public_base_url(company)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{base_url}/jobs",
            json={"appliedFacets": {}, "limit": limit, "offset": 0, "searchText": ""},
        )
        response.raise_for_status()
        data = response.json()
        listings = data.get("jobPostings", [])[:limit]

        jobs: list[dict[str, Any]] = []
        for listing in listings:
            external_path = listing.get("externalPath")
            if not external_path:
                continue
            detail_url = connector._detail_url(base_url, str(external_path))
            detail_response = await client.get(detail_url)
            detail_response.raise_for_status()
            detail = detail_response.json()
            info = detail.get("jobPostingInfo", detail)
            job_req_id = connector._resolve_job_req_id(listing)
            merged = {**listing, **info}
            merged["id"] = job_req_id or listing.get("bulletFields", [None])[0]
            merged["externalLink"] = connector._public_posting_url(
                company, public_base_url, str(external_path)
            )
            jobs.append(merged)
        return jobs


async def _limited_oracle_fetch(connector: OracleHCMConnector, company: Company, limit: int) -> list[dict]:
    import httpx

    base_url = connector._base_url(company)
    site_number = connector._site_number(company)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{base_url}/recruitingCEJobRequisitions",
            params={
                "onlyData": "true",
                "expand": "requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations",
                "finder": f"findReqs;siteNumber={site_number},offset=0,limit={limit}",
            },
            headers=connector._headers(),
        )
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        listings = items[0].get("requisitionList", [])[:limit] if items else []

        jobs: list[dict[str, Any]] = []
        for listing in listings:
            job_id = listing.get("Id")
            if not job_id:
                continue
            detail = await connector._fetch_detail(client, base_url, site_number, str(job_id))
            merged = {**listing, **detail}
            merged["id"] = str(job_id)
            merged["externalLink"] = connector._public_posting_url(company, str(job_id))
            jobs.append(merged)
        return jobs


async def _limited_talentbrew_fetch(
    connector: TalentBrewConnector, company: Company, limit: int
) -> list[dict[str, Any]]:
    import httpx

    base_url = connector._base_url(company)
    company_id = connector._company_id(company)
    headers = {"User-Agent": "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"}
    async with httpx.AsyncClient(timeout=30.0, headers=headers, follow_redirects=True) as client:
        response = await client.get(f"{base_url}/search-jobs/{company_id}/1")
        response.raise_for_status()
        from app.ingestion.connectors.talentbrew import parse_talentbrew_list_page

        summaries, _ = parse_talentbrew_list_page(
            response.text, base_url=base_url, company_id=company_id
        )
        summaries = summaries[:limit]
        jobs: list[dict[str, Any]] = []
        for summary in summaries:
            detail = await connector._fetch_job_detail(client, summary, asyncio.Semaphore(1))
            if detail:
                jobs.append({**summary, **detail})
        return jobs


async def _limited_apple_fetch(
    connector: AppleCareersConnector, company: Company, limit: int
) -> list[dict[str, Any]]:
    import httpx

    base_url = connector._search_base_url(company)
    teams = connector._teams(company)[:1]
    location = connector._location_filter(company)
    headers = {"User-Agent": "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"}
    async with httpx.AsyncClient(timeout=30.0, headers=headers, follow_redirects=True) as client:
        params: dict[str, Any] = {"team": teams[0], "page": 1}
        if location:
            params["location"] = location
        response = await client.get(f"{base_url}/search", params=params)
        response.raise_for_status()
        from app.ingestion.connectors.apple_careers import SITE_ROOT, parse_apple_careers_list_page

        summaries = parse_apple_careers_list_page(response.text, base_url=SITE_ROOT)[:limit]
        jobs: list[dict[str, Any]] = []
        for summary in summaries:
            detail = await connector._fetch_job_detail(client, summary, asyncio.Semaphore(1))
            if detail:
                jobs.append({**summary, **detail})
        return jobs


async def _limited_eightfold_fetch(
    connector: EightfoldConnector, company: Company, limit: int
) -> list[dict[str, Any]]:
    import httpx

    api_host = connector._api_host(company)
    headers = {"User-Agent": "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"}
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        response = await client.get(
            f"https://{api_host}/api/apply/v2/jobs",
            params={**connector._list_params(company, start=0), "num": str(limit)},
        )
        response.raise_for_status()
        data = response.json()
        summaries = [p for p in data.get("positions", []) if isinstance(p, dict)][:limit]
        jobs: list[dict[str, Any]] = []
        for summary in summaries:
            detail = await connector._fetch_job_detail(
                client, api_host, company, summary, asyncio.Semaphore(1)
            )
            if not detail:
                continue
            job_id = summary.get("id")
            merged = {**summary, **detail}
            merged["id"] = str(job_id)
            merged["externalLink"] = connector._public_job_url(company, str(job_id))
            jobs.append(merged)
        return jobs


async def _run_case(case: SmokeCase) -> dict[str, Any]:
    connector = get_connector(case.company.platform)
    started = time.perf_counter()

    if isinstance(connector, WorkdayConnector):
        jobs = await _limited_workday_fetch(connector, case.company, case.detail_limit)
        list_total_hint = "1 list page"
    elif isinstance(connector, OracleHCMConnector):
        jobs = await _limited_oracle_fetch(connector, case.company, case.detail_limit)
        list_total_hint = f"first {case.detail_limit} from list"
    elif isinstance(connector, TalentBrewConnector):
        jobs = await _limited_talentbrew_fetch(connector, case.company, case.detail_limit)
        list_total_hint = "search-jobs page 1+"
    elif isinstance(connector, AppleCareersConnector):
        jobs = await _limited_apple_fetch(connector, case.company, case.detail_limit)
        list_total_hint = "1 team, page 1+"
    elif isinstance(connector, EightfoldConnector):
        jobs = await _limited_eightfold_fetch(connector, case.company, case.detail_limit)
        list_total_hint = "full API list (limited details)"
    else:
        jobs = await connector.fetch_jobs(case.company)
        list_total_hint = "full fetch"

    elapsed = time.perf_counter() - started
    sample = _sample_from_job(jobs[0]) if jobs else None

    return {
        "label": case.label,
        "status": "ok",
        "jobs_with_details": len(jobs),
        "scope": list_total_hint,
        "elapsed_seconds": round(elapsed, 1),
        "sample": sample,
    }


async def main() -> int:
    results: list[dict[str, Any]] = []
    failures = 0

    print("Running live connector smoke tests (limited to 3 jobs each)...\n")

    for case in SMOKE_CASES:
        print(f"→ {case.label} ...", flush=True)
        try:
            result = await asyncio.wait_for(_run_case(case), timeout=120.0)
            results.append(result)
            sample = result.get("sample") or {}
            print(
                f"  OK: {result['jobs_with_details']} jobs w/ details in {result['elapsed_seconds']}s"
                f" | {sample.get('title', 'n/a')}"
            )
            if sample.get("url"):
                print(f"     url: {sample['url']}")
            if sample.get("description_chars") is not None:
                print(f"     description: {sample['description_chars']} chars")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            results.append({"label": case.label, "status": "error", "error": str(exc)})
            print(f"  FAIL: {exc}")

    print("\n--- Summary ---")
    print(json.dumps(results, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
