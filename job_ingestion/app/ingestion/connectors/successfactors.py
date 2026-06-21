from __future__ import annotations

import asyncio
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlencode, urljoin, urlparse

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

DETAIL_DELAY = 2.0
SITEMAP_NAMESPACES = (
    "http://www.google.com/schemas/sitemap/0.9",
    "http://www.sitemaps.org/schemas/sitemap/0.9",
)
JOB_URL_PATTERN = re.compile(r"/job/[^/]+/(\d+)/?")
RMK_DATE_POSTED = re.compile(
    r"^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+"
    r"\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+UTC\s+\d{4}$"
)

BROWSER_IMPERSONATE = "chrome120"
REQUEST_TIMEOUT = 30.0
DEFAULT_SEARCH_PAGE_SIZE = 10


def extract_job_id_from_url(url: str) -> Optional[str]:
    match = JOB_URL_PATTERN.search(urlparse(url).path)
    return match.group(1) if match else None


def is_job_detail_url(url: str) -> bool:
    return bool(JOB_URL_PATTERN.search(urlparse(url).path))


def _response_content(response: Any) -> bytes:
    content = response.content
    if isinstance(content, bytes):
        return content
    return str(content).encode()


def _meta_content(soup: BeautifulSoup, itemprop: str) -> Optional[str]:
    tag = soup.find("meta", attrs={"itemprop": itemprop})
    if tag and tag.get("content"):
        return str(tag["content"]).strip() or None
    return None


def _extract_title(soup: BeautifulSoup) -> Optional[str]:
    title_el = soup.find(attrs={"itemprop": "title"})
    if title_el:
        text = title_el.get_text(strip=True)
        if text:
            return text

    link = soup.select_one("a.jobTitle-link")
    if link:
        text = link.get_text(strip=True)
        if text:
            return text

    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else None


def _extract_location(soup: BeautifulSoup) -> Optional[str]:
    location_el = soup.find(id="job-location")
    if location_el:
        text = location_el.get_text(" ", strip=True)
        if text:
            return text.replace("Location:", "", 1).strip() or None

    locality = _meta_content(soup, "addressLocality")
    region = _meta_content(soup, "addressRegion")
    country = _meta_content(soup, "addressCountry")
    postal = _meta_content(soup, "postalCode")
    parts = [part for part in (locality, region, postal, country) if part]
    if parts:
        return ", ".join(parts)
    return None


def _extract_date_posted(soup: BeautifulSoup) -> Optional[str]:
    posted = _meta_content(soup, "datePosted")
    if posted:
        return posted

    date_el = soup.find(id="job-date")
    if date_el:
        text = date_el.get_text(" ", strip=True)
        if text:
            cleaned = text.replace("Date:", "", 1).strip()
            return cleaned or None
    return None


def _extract_description_html(soup: BeautifulSoup) -> str:
    description_el = soup.find(attrs={"itemprop": "description"})
    if description_el:
        job_desc = description_el.find(class_="jobdescription")
        if job_desc:
            inner = job_desc.decode_contents().strip()
            if inner:
                return inner
        inner = description_el.decode_contents().strip()
        if inner:
            return inner

    job_desc = soup.find(class_="jobdescription")
    if job_desc:
        return job_desc.decode_contents().strip()
    return ""


def parse_successfactors_detail_html(html: bytes | str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    return {
        "title": _extract_title(soup),
        "location": _extract_location(soup),
        "datePosted": _extract_date_posted(soup),
        "raw_html": _extract_description_html(soup),
    }


def parse_successfactors_date_posted(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    stripped = value.strip()
    if RMK_DATE_POSTED.match(stripped):
        try:
            return datetime.strptime(stripped, "%a %b %d %H:%M:%S UTC %Y").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            pass
    for fmt in ("%b %d, %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(stripped, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    normalized = stripped.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


class SuccessFactorsConnector(BaseConnector):
    detail_delay = DETAIL_DELAY

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _career_site_url(self, company: Company) -> str:
        config = self._platform_config(company)
        if config.get("career_site_url"):
            return str(config["career_site_url"]).rstrip("/")
        raise ParseError(f"SuccessFactors career_site_url missing for {company.board_token}")

    def _search_page_size(self, company: Company) -> int:
        config = self._platform_config(company)
        raw = config.get("search_page_size", DEFAULT_SEARCH_PAGE_SIZE)
        try:
            return max(1, int(raw))
        except (TypeError, ValueError):
            return DEFAULT_SEARCH_PAGE_SIZE

    def _search_params(self, company: Company, *, startrow: int = 0) -> dict[str, str]:
        config = self._platform_config(company)
        params: dict[str, str] = {
            "createNewAlert": "false",
            "q": "",
            "locationsearch": "",
            "sortColumn": "referencedate",
            "sortDirection": "desc",
        }
        locale = config.get("locale")
        if locale:
            params["locale"] = str(locale)
        extra = config.get("search_default_params")
        if isinstance(extra, dict):
            params.update({str(k): str(v) for k, v in extra.items()})
        if startrow > 0:
            params["startrow"] = str(startrow)
        return params

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        base_url = self._career_site_url(company)
        job_entries = await self._fetch_job_entries(company, base_url)
        if not job_entries:
            if structlog:
                logger.warning(
                    "successfactors_empty_job_list",
                    company=company.name,
                    base_url=base_url,
                )
            else:
                logger.warning(
                    "successfactors_empty_job_list company=%s base_url=%s",
                    company.name,
                    base_url,
                )
            return []

        results: list[dict[str, Any]] = []
        async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=REQUEST_TIMEOUT) as client:
            for entry in job_entries:
                job_id = entry["job_id"]
                job_url = entry["url"]
                lastmod = entry.get("lastmod")
                try:
                    detail = await self._fetch_detail(client, job_url)
                    results.append(
                        {
                            "id": job_id,
                            "job_id": job_id,
                            "sitemap_url": job_url,
                            "lastmod": lastmod,
                            "externalLink": job_url,
                            **detail,
                        }
                    )
                except ConnectorFetchError as exc:
                    if structlog:
                        logger.warning(
                            "successfactors_detail_fetch_failed",
                            company=company.name,
                            job_id=job_id,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "successfactors_detail_fetch_failed company=%s job_id=%s error=%s",
                            company.name,
                            job_id,
                            exc,
                        )
                    continue
                except Exception as exc:  # noqa: BLE001
                    if structlog:
                        logger.warning(
                            "successfactors_detail_unexpected",
                            company=company.name,
                            job_id=job_id,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "successfactors_detail_unexpected company=%s job_id=%s error=%s",
                            company.name,
                            job_id,
                            exc,
                        )
                    continue
                await asyncio.sleep(self.detail_delay)

        return results

    async def _fetch_job_entries(self, company: Company, base_url: str) -> list[dict[str, Any]]:
        sitemap_url = f"{base_url}/sitemap.xml"
        async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(sitemap_url)

        if response.status_code in (403, 404, 405):
            if structlog:
                logger.info(
                    "successfactors_sitemap_unavailable_will_paginate",
                    url=sitemap_url,
                    status_code=response.status_code,
                )
            else:
                logger.info(
                    "successfactors_sitemap_unavailable_will_paginate url=%s status_code=%s",
                    sitemap_url,
                    response.status_code,
                )
            return await self._fetch_via_search_pagination(company, base_url)

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"SuccessFactors sitemap failed: {response.status_code}",
                response.status_code,
            )

        try:
            root = ET.fromstring(_response_content(response))
        except ET.ParseError as exc:
            raise ParseError(f"SuccessFactors sitemap XML parse error: {exc}") from exc

        entries: list[dict[str, Any]] = []
        url_elements: list[Any] = []
        for namespace in SITEMAP_NAMESPACES:
            url_elements = root.findall(f"{{{namespace}}}url")
            if url_elements:
                break
        if not url_elements:
            url_elements = [el for el in root if el.tag.endswith("url")]

        for url_el in url_elements:
            loc_el = None
            lastmod_el = None
            for namespace in SITEMAP_NAMESPACES:
                if loc_el is None:
                    loc_el = url_el.find(f"{{{namespace}}}loc")
                if lastmod_el is None:
                    lastmod_el = url_el.find(f"{{{namespace}}}lastmod")
            if loc_el is None:
                loc_el = next((el for el in url_el if el.tag.endswith("loc")), None)
            if lastmod_el is None:
                lastmod_el = next((el for el in url_el if el.tag.endswith("lastmod")), None)
            if loc_el is None:
                continue

            loc = loc_el.text or ""
            if not is_job_detail_url(loc):
                continue

            job_id = extract_job_id_from_url(loc)
            if not job_id:
                continue

            entries.append(
                {
                    "job_id": job_id,
                    "url": loc,
                    "lastmod": lastmod_el.text if lastmod_el is not None else None,
                }
            )

        return entries

    async def _fetch_via_search_pagination(
        self,
        company: Company,
        base_url: str,
    ) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        page_size = self._search_page_size(company)
        startrow = 0

        async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=REQUEST_TIMEOUT) as client:
            while startrow <= 5000:
                params = self._search_params(company, startrow=startrow)
                search_url = f"{base_url}/search/?{urlencode(params)}"
                response = await client.get(search_url)
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(_response_content(response), "html.parser")
                links = soup.select("a.jobTitle-link[href*='/job/']")
                if not links:
                    break

                page_had_new = False
                for link in links:
                    href = link.get("href", "")
                    if not href:
                        continue
                    job_url = urljoin(base_url, href)
                    if not is_job_detail_url(job_url):
                        continue
                    job_id = extract_job_id_from_url(job_url)
                    if not job_id or job_id in seen_ids:
                        continue
                    seen_ids.add(job_id)
                    entries.append({"job_id": job_id, "url": job_url, "lastmod": None})
                    page_had_new = True

                if not page_had_new or len(links) < page_size:
                    break

                startrow += page_size
                await asyncio.sleep(self.detail_delay)

        return entries

    async def _fetch_detail(self, client: AsyncSession, job_url: str) -> dict[str, Any]:
        response = await client.get(job_url)

        if response.status_code == 429:
            await asyncio.sleep(5.0)
            response = await client.get(job_url)

        if response.status_code == 404:
            raise ConnectorFetchError(f"SuccessFactors job 404: {job_url}", 404)

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"SuccessFactors detail failed {response.status_code}: {job_url}",
                response.status_code,
            )

        parsed = parse_successfactors_detail_html(_response_content(response))
        parsed["detail_url"] = job_url
        return parsed
