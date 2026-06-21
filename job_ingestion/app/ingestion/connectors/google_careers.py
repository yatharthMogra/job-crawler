from __future__ import annotations

import asyncio
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

LIST_URL = "https://www.google.com/about/careers/applications/jobs/results"
BASE_URL = "https://www.google.com/about/careers/applications/"
DETAIL_CONCURRENCY = 4
DETAIL_DELAY = 1.0
REQUEST_TIMEOUT = 30.0
PAGE_SIZE = 20
USER_AGENT = "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"

JOB_LINK_PATTERN = re.compile(r"jobs/results/(\d+)-")
PAGINATION_PATTERN = re.compile(r"Showing \d+ to \d+ of ([\d,]+) rows")
DETAIL_SECTIONS = (
    "Minimum qualifications",
    "Preferred qualifications",
    "About the job",
    "Responsibilities",
)


def extract_job_id_from_url(url: str) -> Optional[str]:
    match = JOB_LINK_PATTERN.search(url)
    return match.group(1) if match else None


def _absolute_detail_url(href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return urljoin(BASE_URL, href.lstrip("/"))


def _parse_pagination_total(html: str) -> Optional[int]:
    match = PAGINATION_PATTERN.search(html)
    if not match:
        return None
    try:
        return int(match.group(1).replace(",", ""))
    except ValueError:
        return None


def _extract_card_location(card: BeautifulSoup) -> str:
    loc_container = card.select_one(".op1BBf .pwO9Dc") or card.select_one(".pwO9Dc")
    if not loc_container:
        return ""
    parts: list[str] = []
    for span in loc_container.select("span.r0wTof, span.BVHzed"):
        text = span.get_text(strip=True)
        if text:
            parts.append(text)
    return "".join(parts)


def _extract_card_organization(card: BeautifulSoup) -> str:
    org_span = card.select_one("span.RP7SMd span")
    if org_span:
        text = org_span.get_text(strip=True)
        if text:
            return text
    return "Google"


def _extract_card_experience_level(card: BeautifulSoup) -> Optional[str]:
    exp_span = card.select_one("span.wVSTAb")
    if not exp_span:
        return None
    text = exp_span.get_text(strip=True)
    return text or None


def _extract_card_title(card: BeautifulSoup, link: BeautifulSoup) -> str:
    title_el = card.select_one("h3.QJPWVe") or card.find("h3")
    if title_el:
        text = title_el.get_text(strip=True)
        if text:
            return text
    aria = link.get("aria-label", "")
    prefix = "Learn more about "
    if isinstance(aria, str) and aria.startswith(prefix):
        return aria[len(prefix) :].strip()
    return ""


def _extract_list_min_qualifications(card: BeautifulSoup) -> str:
    heading = card.find("h4", string=re.compile(r"Minimum qualifications", re.I))
    if not heading:
        return ""
    ul = heading.find_next("ul")
    if not ul:
        return ""
    return ul.decode_contents().strip()


def parse_google_careers_list_page(html: str) -> tuple[list[dict[str, Any]], Optional[int]]:
    soup = BeautifulSoup(html, "html.parser")
    total = _parse_pagination_total(html)
    summaries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    links = soup.find_all(
        "a",
        href=JOB_LINK_PATTERN,
        attrs={"aria-label": re.compile(r"^Learn more about ")},
    )
    for link in links:
        href = link.get("href")
        if not href:
            continue
        job_id = extract_job_id_from_url(href)
        if not job_id or job_id in seen_ids:
            continue
        seen_ids.add(job_id)

        card = link.find_parent("li")
        if card is None:
            card = link

        summaries.append(
            {
                "id": job_id,
                "title": _extract_card_title(card, link),
                "organization": _extract_card_organization(card),
                "location": _extract_card_location(card),
                "experience_level": _extract_card_experience_level(card),
                "externalLink": _absolute_detail_url(href),
                "list_min_qualifications": _extract_list_min_qualifications(card),
            }
        )

    return summaries, total


def _section_heading_pattern(section_name: str) -> re.Pattern[str]:
    return re.compile(rf"^{re.escape(section_name)}:?$", re.I)


def parse_google_careers_detail_html(
    html: str,
    *,
    experience_level: Optional[str] = None,
    list_min_qualifications: str = "",
) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    sections: list[str] = []

    if experience_level:
        sections.append(f"<p><strong>Experience level:</strong> {experience_level}</p>")

    for section_name in DETAIL_SECTIONS:
        pattern = _section_heading_pattern(section_name)
        headings = soup.find_all(["h2", "h3", "h4"], string=pattern)
        if not headings:
            continue
        heading = headings[-1]
        content: list[str] = []
        for sibling in heading.find_next_siblings():
            if sibling.name in ("h2", "h3", "h4"):
                break
            content.append(str(sibling))
        if content:
            sections.append(f"<h3>{section_name}</h3>{''.join(content)}")

    raw_html = "\n".join(sections)
    if not raw_html and list_min_qualifications:
        raw_html = f"<h3>Minimum qualifications</h3><ul>{list_min_qualifications}</ul>"

    return {"raw_html": raw_html}


class GoogleCareersConnector(BaseConnector):
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        headers = {"User-Agent": USER_AGENT}
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, headers=headers) as client:
                summaries, total_advertised = await self._fetch_all_summaries(client)
                if not summaries:
                    return []

                if total_advertised is not None and len(summaries) < total_advertised:
                    if structlog:
                        logger.warning(
                            "google_careers_list_incomplete",
                            board_token=company.board_token,
                            found=len(summaries),
                            advertised=total_advertised,
                        )
                    else:
                        logger.warning(
                            "google_careers_list_incomplete board_token=%s found=%s advertised=%s",
                            company.board_token,
                            len(summaries),
                            total_advertised,
                        )

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
                f"Google Careers fetch failed for {company.board_token}: {exc}"
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
    ) -> tuple[list[dict[str, Any]], Optional[int]]:
        all_summaries: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        total_advertised: Optional[int] = None
        page = 1

        while True:
            response = await client.get(LIST_URL, params={"page": page})
            response.raise_for_status()
            page_summaries, page_total = parse_google_careers_list_page(response.text)

            if page_total is not None:
                total_advertised = page_total

            new_summaries = [
                summary
                for summary in page_summaries
                if summary["id"] not in seen_ids
            ]
            for summary in new_summaries:
                seen_ids.add(summary["id"])
            all_summaries.extend(new_summaries)

            if not page_summaries or not new_summaries:
                break
            if total_advertised is not None and page * PAGE_SIZE >= total_advertised:
                break
            page += 1

        return all_summaries, total_advertised

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
                    if structlog:
                        logger.debug("google_careers_detail_not_found", job_id=job_id)
                    else:
                        logger.debug("google_careers_detail_not_found job_id=%s", job_id)
                    return None
                response.raise_for_status()
                parsed = parse_google_careers_detail_html(
                    response.text,
                    experience_level=summary.get("experience_level"),
                    list_min_qualifications=summary.get("list_min_qualifications") or "",
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                raise ConnectorFetchError(
                    f"Google Careers detail failed for {job_id}: {exc}"
                ) from exc
            except Exception as exc:  # noqa: BLE001
                raise ConnectorFetchError(
                    f"Google Careers detail failed for {job_id}: {exc}"
                ) from exc
            finally:
                await asyncio.sleep(self.detail_delay)

        return parsed
