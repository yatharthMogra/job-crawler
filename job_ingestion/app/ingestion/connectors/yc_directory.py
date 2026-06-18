from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import httpx

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.config import Settings, get_settings

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

YC_COMPANIES_URL = "https://api.ycombinator.com/v0.1/companies"

ATS_FINGERPRINTS: dict[str, list[str]] = {
    "greenhouse": [
        r"boards\.greenhouse\.io/([^/\"'\s]+)",
        r"job-boards\.greenhouse\.io/([^/\"'\s]+)",
    ],
    "lever": [r"jobs\.lever\.co/([^/\"'\s]+)"],
    "ashby": [
        r"jobs\.ashbyhq\.com/([^/\"'\s]+)",
        r"jobs\.ashby\.com/([^/\"'\s]+)",
    ],
    "workday": [r"([\w-]+)\.wd(\d+)\.myworkdayjobs\.com"],
}


@dataclass
class WorkdayDiscovery:
    tenant: str
    instance: str
    board_token: str


@dataclass
class DirectoryCrawlResult:
    greenhouse_tokens: list[str] = field(default_factory=list)
    lever_slugs: list[str] = field(default_factory=list)
    ashby_slugs: list[str] = field(default_factory=list)
    workday_discoveries: list[WorkdayDiscovery] = field(default_factory=list)
    yc_native_companies: list[dict[str, Any]] = field(default_factory=list)
    unresolved: list[dict[str, Any]] = field(default_factory=list)
    skipped_existing: int = 0


async def fetch_all_yc_companies(client: httpx.AsyncClient) -> list[dict[str, Any]]:
    companies: list[dict[str, Any]] = []
    page = 1
    while True:
        resp = await client.get(YC_COMPANIES_URL, params={"page": page})
        resp.raise_for_status()
        payload = resp.json()
        batch = payload if isinstance(payload, list) else payload.get("companies") or payload.get("results") or []
        if not isinstance(batch, list) or not batch:
            break
        companies.extend(item for item in batch if isinstance(item, dict))
        if len(batch) < 50:
            break
        page += 1
        await asyncio.sleep(0.3)
    return companies


def derive_career_urls(website: str) -> list[str]:
    parsed = urlparse(website if "://" in website else f"https://{website}")
    if not parsed.netloc:
        return []
    scheme = parsed.scheme or "https"
    base = f"{scheme}://{parsed.netloc}".rstrip("/")
    return [
        f"{base}/careers",
        f"{base}/jobs",
        f"{base}/about/careers",
        base,
    ]


def detect_ats_from_html(html: str) -> tuple[str | None, str | None, WorkdayDiscovery | None]:
    for ats, patterns in ATS_FINGERPRINTS.items():
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if not match:
                continue
            if ats == "workday":
                tenant = match.group(1)
                instance = match.group(2)
                return ats, tenant, WorkdayDiscovery(
                    tenant=tenant,
                    instance=f"wd{instance}",
                    board_token=tenant,
                )
            return ats, match.group(1), None
    return None, None, None


async def probe_for_ats(
    client: httpx.AsyncClient,
    urls: list[str],
) -> tuple[str | None, str | None, WorkdayDiscovery | None]:
    for url in urls:
        try:
            resp = await client.get(url, timeout=10.0)
            if resp.status_code >= 400:
                continue
            return detect_ats_from_html(resp.text)
        except Exception:  # noqa: BLE001
            continue
    return None, None, None


async def crawl_yc_directory(
    *,
    settings: Settings | None = None,
    existing_tokens: set[str] | None = None,
) -> DirectoryCrawlResult:
    settings = settings or get_settings()
    existing = existing_tokens or set()
    result = DirectoryCrawlResult()
    probe_sem = asyncio.Semaphore(max(settings.yc_directory_probe_concurrency, 1))
    probe_delay = 0.5

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        companies = await fetch_all_yc_companies(client)
        hiring = [company for company in companies if company.get("hiring")]

        async def _probe_company(company: dict[str, Any]) -> None:
            async with probe_sem:
                website = (company.get("website") or "").strip()
                if not website:
                    result.yc_native_companies.append(company)
                    return

                ats_type, identifier, workday = await probe_for_ats(client, derive_career_urls(website))
                await asyncio.sleep(probe_delay)

                if ats_type == "greenhouse" and identifier:
                    if identifier in existing:
                        result.skipped_existing += 1
                        return
                    result.greenhouse_tokens.append(identifier)
                    existing.add(identifier)
                elif ats_type == "lever" and identifier:
                    if identifier in existing:
                        result.skipped_existing += 1
                        return
                    result.lever_slugs.append(identifier)
                    existing.add(identifier)
                elif ats_type == "ashby" and identifier:
                    if identifier in existing:
                        result.skipped_existing += 1
                        return
                    result.ashby_slugs.append(identifier)
                    existing.add(identifier)
                elif ats_type == "workday" and workday is not None:
                    if workday.board_token in existing:
                        result.skipped_existing += 1
                        return
                    result.workday_discoveries.append(workday)
                    existing.add(workday.board_token)
                else:
                    result.yc_native_companies.append(company)

        await asyncio.gather(*[_probe_company(company) for company in hiring])

    return result
