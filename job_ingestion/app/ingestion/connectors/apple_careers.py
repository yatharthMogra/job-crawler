from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any, Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

DETAIL_CONCURRENCY = 4
DETAIL_DELAY = 0.5
REQUEST_TIMEOUT = 30.0
USER_AGENT = "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"

DETAIL_HREF_PATTERN = re.compile(r"/details/(\d{9}-\d{4})/")
HYDRATION_PATTERN = re.compile(
    r'window\.__staticRouterHydrationData = JSON\.parse\("(.+?)"\)',
    re.DOTALL,
)
SITE_ROOT = "https://jobs.apple.com"
DETAIL_SECTIONS = (
    "Summary",
    "Description",
    "Responsibilities",
    "Minimum Qualifications",
    "Preferred Qualifications",
    "Key Qualifications",
)

DEFAULT_TEAMS = [
    "apps-and-frameworks-SFTWR-AF",
    "software-quality-automation-and-tools-SFTWR-SQAT",
    "cloud-and-infrastructure-SFTWR-CLD",
]


def _absolute_url(href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return urljoin(SITE_ROOT + "/", href.lstrip("/"))


def _title_from_aria(aria: str) -> str:
    cleaned = aria.strip()
    cleaned = re.sub(r"\s+\d{9}(?:-\d{4})?\s*$", "", cleaned)
    return cleaned.strip()


def _parse_hydration_json(html: str) -> dict[str, Any] | None:
    match = HYDRATION_PATTERN.search(html)
    if not match:
        return None
    try:
        raw = match.group(1).encode().decode("unicode_escape")
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    job_details = data.get("loaderData", {}).get("jobDetails", {})
    jobs_data = job_details.get("jobsData")
    if not isinstance(jobs_data, dict):
        return None

    locale = jobs_data.get("selectedLocale") or "en_US"
    localizations = jobs_data.get("localizations", {})
    posting = localizations.get(locale, {}).get("posting", {})
    if not isinstance(posting, dict):
        posting = {}

    locations = jobs_data.get("locations") or []
    location_names: list[str] = []
    if isinstance(locations, list):
        for loc in locations:
            if isinstance(loc, dict) and loc.get("name"):
                location_names.append(str(loc["name"]))

    sections: list[str] = []
    for label, key in (
        ("Summary", "jobSummary"),
        ("Description", "description"),
        ("Minimum Qualifications", "minimumQualifications"),
        ("Preferred Qualifications", "preferredQualifications"),
    ):
        value = posting.get(key) or jobs_data.get(key)
        if value:
            sections.append(f"<h3>{label}</h3><p>{value}</p>")

    return {
        "title": posting.get("postingTitle") or jobs_data.get("postingTitle"),
        "location": " | ".join(location_names) or None,
        "raw_html": "\n".join(sections),
    }


def parse_apple_careers_list_page(html: str, *, base_url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    summaries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for link in soup.select("a[href*='/details/']"):
        href = link.get("href")
        if not href:
            continue
        match = DETAIL_HREF_PATTERN.search(href)
        if not match:
            continue
        role_id = match.group(1)
        if role_id in seen_ids:
            continue
        seen_ids.add(role_id)

        title = ""
        aria = link.get("aria-label", "")
        if isinstance(aria, str) and aria.strip():
            title = _title_from_aria(aria)
        if not title:
            title_el = link.find("h3")
            if title_el:
                title = title_el.get_text(strip=True)

        location = ""
        card = link.find_parent("li") or link.find_parent(class_=re.compile("job-list-item"))
        if card:
            loc_el = card.select_one(".job-location") or card.select_one("[class*='location']")
            if loc_el:
                location = loc_el.get_text(" ", strip=True)

        summaries.append(
            {
                "id": role_id,
                "title": title,
                "location": location or None,
                "externalLink": _absolute_url(href),
            }
        )

    return summaries


def parse_apple_careers_detail_html(html: str) -> dict[str, Any]:
    hydrated = _parse_hydration_json(html)
    if hydrated and hydrated.get("raw_html"):
        return hydrated

    soup = BeautifulSoup(html, "html.parser")
    sections: list[str] = []

    for section_name in DETAIL_SECTIONS:
        headings = soup.find_all(
            ["h2", "h3", "h4", "strong"],
            string=re.compile(rf"^{re.escape(section_name)}:?$", re.I),
        )
        if not headings:
            continue
        heading = headings[0]
        content: list[str] = []
        for sibling in heading.find_next_siblings():
            if sibling.name in ("h2", "h3", "h4"):
                break
            content.append(str(sibling))
        if content:
            sections.append(f"<h3>{section_name}</h3>{''.join(content)}")

    if not sections:
        main = soup.select_one("main") or soup.select_one("[class*='job-description']")
        if main:
            sections.append(main.decode_contents())

    return {"raw_html": "\n".join(sections)}


class AppleCareersConnector(BaseConnector):
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _search_base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        locale = str(config.get("locale", "en-us"))
        return f"https://jobs.apple.com/{locale}"

    def _teams(self, company: Company) -> list[str]:
        config = self._platform_config(company)
        teams = config.get("teams")
        if isinstance(teams, list) and teams:
            return [str(team) for team in teams]
        return list(DEFAULT_TEAMS)

    def _location_filter(self, company: Company) -> Optional[str]:
        config = self._platform_config(company)
        location = config.get("location")
        return str(location) if location else None

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        base_url = self._search_base_url(company)
        teams = self._teams(company)
        location = self._location_filter(company)
        headers = {"User-Agent": USER_AGENT}

        try:
            async with httpx.AsyncClient(
                timeout=REQUEST_TIMEOUT,
                headers=headers,
                follow_redirects=True,
            ) as client:
                summaries = await self._fetch_all_summaries(client, base_url, teams, location)
                if not summaries:
                    return []

                semaphore = asyncio.Semaphore(self.detail_concurrency)
                tasks = [
                    self._fetch_job_detail(client, summary, semaphore)
                    for summary in summaries
                ]
                details = await asyncio.gather(*tasks)
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Apple Careers fetch failed for {company.board_token}: {exc}"
            ) from exc

        jobs: list[dict[str, Any]] = []
        for summary, detail in zip(summaries, details):
            if detail is None:
                continue
            jobs.append({**summary, **detail})
        return jobs

    async def _fetch_all_summaries(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        teams: list[str],
        location: Optional[str],
    ) -> list[dict[str, Any]]:
        all_summaries: list[dict[str, Any]] = []
        seen_ids: set[str] = set()

        for team in teams:
            page = 1
            while True:
                params: dict[str, Any] = {"team": team, "page": page}
                if location:
                    params["location"] = location

                response = await client.get(f"{base_url}/search", params=params)
                response.raise_for_status()
                page_summaries = parse_apple_careers_list_page(response.text, base_url=base_url)

                new_summaries = [
                    summary for summary in page_summaries if summary["id"] not in seen_ids
                ]
                for summary in new_summaries:
                    seen_ids.add(summary["id"])
                all_summaries.extend(new_summaries)

                if not page_summaries or not new_summaries:
                    break
                page += 1

        return all_summaries

    async def _fetch_job_detail(
        self,
        client: httpx.AsyncClient,
        summary: dict[str, Any],
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any] | None:
        detail_url = summary.get("externalLink")
        job_id = summary.get("id")
        if not detail_url or not job_id:
            return None

        async with semaphore:
            try:
                response = await client.get(detail_url)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                parsed = parse_apple_careers_detail_html(response.text)
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                raise ConnectorFetchError(
                    f"Apple Careers detail failed for {job_id}: {exc}"
                ) from exc
            except Exception as exc:  # noqa: BLE001
                raise ConnectorFetchError(
                    f"Apple Careers detail failed for {job_id}: {exc}"
                ) from exc
            finally:
                await asyncio.sleep(self.detail_delay)

        return parsed
