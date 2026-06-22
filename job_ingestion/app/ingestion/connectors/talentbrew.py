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

DETAIL_CONCURRENCY = 5
DETAIL_DELAY = 0.3
REQUEST_TIMEOUT = 30.0
USER_AGENT = "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"

JOB_HREF_PATTERN = re.compile(r"/job/[^/]+/[^/]+/(\d+)/(\d+)")
PAGE_INDICATOR_PATTERN = re.compile(r"page\s+\d+\s*/\s*(\d+)", re.I)


def _absolute_url(base_url: str, href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return urljoin(base_url.rstrip("/") + "/", href.lstrip("/"))


def parse_talentbrew_list_page(html: str, *, base_url: str, company_id: str) -> tuple[list[dict[str, Any]], Optional[int]]:
    soup = BeautifulSoup(html, "html.parser")
    summaries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for link in soup.select("a[href*='/job/']"):
        href = link.get("href")
        if not href:
            continue
        match = JOB_HREF_PATTERN.search(href)
        if not match:
            continue
        if match.group(1) != company_id:
            continue
        job_id = match.group(2)
        if job_id in seen_ids:
            continue
        seen_ids.add(job_id)

        title_el = link.find("h2") or link.find("h3")
        title = title_el.get_text(strip=True) if title_el else link.get_text(strip=True)
        summaries.append(
            {
                "id": job_id,
                "title": title,
                "externalLink": _absolute_url(base_url, href),
            }
        )

    total_pages: Optional[int] = None
    page_indicator = soup.find(string=PAGE_INDICATOR_PATTERN)
    if page_indicator:
        match = PAGE_INDICATOR_PATTERN.search(str(page_indicator))
        if match:
            total_pages = int(match.group(1))

    return summaries, total_pages


def parse_talentbrew_detail_html(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    description_el = (
        soup.select_one("[class*='job-description']")
        or soup.select_one("[class*='description']")
        or soup.select_one("main")
    )
    location = None
    for label in soup.find_all(string=re.compile(r"^Location:?\s*$", re.I)):
        parent = label.find_parent()
        if parent is None:
            continue
        sibling = parent.find_next_sibling()
        if sibling:
            location = sibling.get_text(" ", strip=True)
            break

    raw_html = description_el.decode_contents().strip() if description_el else ""
    return {"location": location, "raw_html": raw_html}


class TalentBrewConnector(BaseConnector):
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        return str(config.get("base_url", "")).rstrip("/")

    def _company_id(self, company: Company) -> str:
        config = self._platform_config(company)
        company_id = config.get("company_id")
        if not company_id:
            raise ParseError(f"TalentBrew company_id missing for {company.name}")
        return str(company_id)

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        base_url = self._base_url(company)
        company_id = self._company_id(company)
        if not base_url:
            raise ParseError(f"TalentBrew base_url missing for {company.name}")

        headers = {"User-Agent": USER_AGENT}
        try:
            async with httpx.AsyncClient(
                timeout=REQUEST_TIMEOUT,
                headers=headers,
                follow_redirects=True,
            ) as client:
                summaries = await self._fetch_all_summaries(client, base_url, company_id)
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
                f"TalentBrew fetch failed for {company.board_token}: {exc}"
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
        company_id: str,
    ) -> list[dict[str, Any]]:
        all_summaries: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        page = 1
        total_pages: Optional[int] = None

        while True:
            url = f"{base_url}/search-jobs/{company_id}/{page}"
            response = await client.get(url)
            if response.status_code == 404:
                break
            response.raise_for_status()

            page_summaries, page_total_pages = parse_talentbrew_list_page(
                response.text,
                base_url=base_url,
                company_id=company_id,
            )
            if page_total_pages is not None:
                total_pages = page_total_pages

            new_summaries = [
                summary for summary in page_summaries if summary["id"] not in seen_ids
            ]
            for summary in new_summaries:
                seen_ids.add(summary["id"])
            all_summaries.extend(new_summaries)

            if not page_summaries or not new_summaries:
                break
            if total_pages is not None and page >= total_pages:
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
                parsed = parse_talentbrew_detail_html(response.text)
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                raise ConnectorFetchError(
                    f"TalentBrew detail failed for {job_id}: {exc}"
                ) from exc
            except Exception as exc:  # noqa: BLE001
                raise ConnectorFetchError(
                    f"TalentBrew detail failed for {job_id}: {exc}"
                ) from exc
            finally:
                await asyncio.sleep(self.detail_delay)

        return parsed
