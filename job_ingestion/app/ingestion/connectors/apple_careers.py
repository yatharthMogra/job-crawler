from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import datetime, timezone
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
DETAIL_MAX_ATTEMPTS = 2
REQUEST_TIMEOUT = 45.0
USER_AGENT = "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"

DETAIL_HREF_PATTERN = re.compile(r"/details/(\d{9}-\d{4})/")
POSTED_DATE_PATTERN = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2},\s+\d{4}\b"
)
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


def _format_fetch_error(exc: BaseException) -> str:
    message = str(exc).strip()
    name = type(exc).__name__
    return f"{name}: {message}" if message else name


def parse_apple_posted_date(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(int(value) / 1000 if value > 10_000_000_000 else int(value), tz=timezone.utc)
        except (TypeError, ValueError, OSError):
            return None
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped:
        return None
    match = POSTED_DATE_PATTERN.search(stripped)
    candidate = match.group(0) if match else stripped
    try:
        parsed = datetime.strptime(candidate, "%B %d, %Y")
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc)


def _posted_date_from_card(card: BeautifulSoup) -> datetime | None:
    if card is None:
        return None
    date_el = card.select_one("[class*='posting-date']") or card.select_one("[class*='posted']")
    if date_el:
        parsed = parse_apple_posted_date(date_el.get_text(" ", strip=True))
        if parsed is not None:
            return parsed
    return parse_apple_posted_date(card.get_text(" ", strip=True))


def _posted_date_from_hydration(posting: dict[str, Any], jobs_data: dict[str, Any]) -> datetime | None:
    for key in ("postingDate", "postDate", "postedDate", "startDate"):
        for source in (posting, jobs_data):
            parsed = parse_apple_posted_date(source.get(key))
            if parsed is not None:
                return parsed
    return None


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
        "posted_at": _posted_date_from_hydration(posting, jobs_data),
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

        posted_at = _posted_date_from_card(card) if card else None
        summary: dict[str, Any] = {
            "id": role_id,
            "title": title,
            "location": location or None,
            "externalLink": _absolute_url(href),
        }
        if posted_at is not None:
            summary["posted_at"] = posted_at
        summaries.append(summary)

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
                details = await asyncio.gather(*tasks, return_exceptions=True)
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Apple Careers fetch failed for {company.board_token}: {_format_fetch_error(exc)}"
            ) from exc

        jobs: list[dict[str, Any]] = []
        detail_failures = 0
        for summary, detail in zip(summaries, details):
            if isinstance(detail, BaseException):
                detail_failures += 1
                self._log_detail_fetch_failed(summary.get("id"), detail)
                continue
            if detail is None:
                continue
            jobs.append({**summary, **detail})
        if detail_failures:
            if structlog:
                logger.warning(
                    "apple_careers_partial_detail_failures",
                    board_token=company.board_token,
                    failed_count=detail_failures,
                    succeeded_count=len(jobs),
                    total_summaries=len(summaries),
                )
            else:
                logger.warning(
                    "apple_careers_partial_detail_failures board_token=%s failed=%s succeeded=%s total=%s",
                    company.board_token,
                    detail_failures,
                    len(jobs),
                    len(summaries),
                )
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

    @staticmethod
    def _log_detail_fetch_failed(job_id: object, exc: BaseException) -> None:
        job_id_str = str(job_id) if job_id is not None else "unknown"
        error = _format_fetch_error(exc)
        if structlog:
            logger.warning(
                "apple_careers_detail_fetch_failed",
                job_id=job_id_str,
                error=error,
                exc_type=type(exc).__name__,
            )
        else:
            logger.warning(
                "apple_careers_detail_fetch_failed job_id=%s error=%s exc_type=%s",
                job_id_str,
                error,
                type(exc).__name__,
            )

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

        last_error: BaseException | None = None
        for attempt in range(1, DETAIL_MAX_ATTEMPTS + 1):
            async with semaphore:
                try:
                    response = await client.get(detail_url)
                    if response.status_code == 404:
                        return None
                    response.raise_for_status()
                    parsed = parse_apple_careers_detail_html(response.text)
                    if summary.get("posted_at") and not parsed.get("posted_at"):
                        parsed["posted_at"] = summary["posted_at"]
                    return parsed
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code == 404:
                        return None
                    last_error = exc
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                finally:
                    await asyncio.sleep(self.detail_delay)
            if attempt < DETAIL_MAX_ATTEMPTS:
                await asyncio.sleep(self.detail_delay)

        if last_error is not None:
            raise last_error
        return None
