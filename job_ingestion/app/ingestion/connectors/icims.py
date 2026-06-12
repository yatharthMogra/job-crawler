from __future__ import annotations

import asyncio
import logging
import re
import xml.etree.ElementTree as ET
from typing import Any, Optional
from urllib.parse import urlparse

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
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
JOB_URL_PATTERN = re.compile(r"/jobs/\d+/.+/job$")
JOB_ID_PATTERN = re.compile(r"/jobs/(\d+)/")

BROWSER_IMPERSONATE = "chrome120"
REQUEST_TIMEOUT = 30.0


def _extract_job_id_from_url(url: str) -> Optional[str]:
    match = JOB_ID_PATTERN.search(url)
    return match.group(1) if match else None


def _job_url_path(url: str) -> str:
    return urlparse(url).path.rstrip("/")


def _is_job_detail_url(url: str) -> bool:
    return bool(JOB_URL_PATTERN.search(_job_url_path(url)))


def _find_field_after_label(soup: BeautifulSoup, label_text: str) -> Optional[str]:
    lowered = label_text.lower()

    for label in soup.find_all(class_="iCIMS_Expandable_Label"):
        if lowered in label.get_text(strip=True).lower():
            value_el = label.find_next(class_="iCIMS_Expandable_Field")
            if value_el:
                return value_el.get_text(strip=True) or None

    for field in soup.find_all(class_="iCIMS_JobHeaderField"):
        if lowered in field.get_text(strip=True).lower():
            value_el = field.find_next(class_="iCIMS_JobHeaderData")
            if value_el:
                return value_el.get_text(strip=True) or None

    for el in soup.find_all(string=lambda t: t and lowered in t.lower()):
        parent = el.parent
        if parent is None:
            continue
        sibling = parent.find_next_sibling()
        if sibling:
            text = sibling.get_text(strip=True)
            if text:
                return text

    return None


def _extract_location(soup: BeautifulSoup) -> Optional[str]:
    for label in soup.find_all("span", class_="sr-only field-label"):
        if "job locations" not in label.get_text(strip=True).lower():
            continue
        sibling = label.next_sibling
        while sibling is not None:
            if isinstance(sibling, str):
                text = sibling.strip()
                if text:
                    return text
            elif getattr(sibling, "name", None) is not None:
                text = sibling.get_text(strip=True)
                if text:
                    return text
            sibling = sibling.next_sibling

    for label in ("Job Locations", "Location", "Job Location"):
        val = _find_field_after_label(soup, label)
        if val:
            return val
    return None


def _extract_title(soup: BeautifulSoup) -> Optional[str]:
    header = soup.find(id="iCIMS_Header")
    if header:
        h1 = header.find("h1")
        if h1:
            return h1.get_text(strip=True) or None

    h1 = soup.find("h1", class_=lambda c: c and "iCIMS" in c)
    if not h1:
        h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else None


def _extract_description_html(soup: BeautifulSoup) -> str:
    text_blocks = soup.find_all(class_="iCIMS_Expandable_Text")
    if text_blocks:
        parts: list[str] = []
        for block in text_blocks:
            inner = block.decode_contents().strip()
            if inner:
                parts.append(inner)
        if parts:
            return "\n".join(parts)

    containers = soup.find_all(class_="iCIMS_Expandable_Container")
    if not containers:
        containers = soup.find_all(
            lambda tag: tag.name == "div"
            and any(
                "description" in str(value).lower()
                for value in [tag.get("id", ""), tag.get("class", "")]
            )
        )

    parts = []
    for container in containers:
        inner = container.decode_contents().strip()
        if inner:
            parts.append(inner)
    return "\n".join(parts)


def _extract_employment_type(soup: BeautifulSoup) -> Optional[str]:
    for label in ("Type", "Job Type", "Employment Type", "Schedule", "Position Type"):
        val = _find_field_after_label(soup, label)
        if val:
            return val
    return None


def _extract_department(soup: BeautifulSoup) -> Optional[str]:
    for label in ("Category", "Department", "Job Category", "Function"):
        val = _find_field_after_label(soup, label)
        if val:
            return val
    return None


def _response_content(response: Any) -> bytes:
    content = response.content
    if isinstance(content, bytes):
        return content
    return str(content).encode()


def _parse_detail_html(html: bytes | str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    return {
        "title": _extract_title(soup),
        "location": _extract_location(soup),
        "department": _extract_department(soup),
        "employment_type_raw": _extract_employment_type(soup),
        "raw_html": _extract_description_html(soup),
    }


class ICIMSConnector(BaseConnector):
    detail_delay = DETAIL_DELAY

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        if config.get("base_url"):
            return str(config["base_url"]).rstrip("/")
        pattern = config.get("url_pattern", "careers-{slug}")
        subdomain = str(pattern).replace("{slug}", company.board_token)
        return f"https://{subdomain}.icims.com"

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        base_url = self._base_url(company)
        job_entries = await self._fetch_sitemap(base_url)
        if not job_entries:
            if structlog:
                logger.warning("icims_empty_sitemap", company=company.name, base_url=base_url)
            else:
                logger.warning(
                    "icims_empty_sitemap company=%s base_url=%s",
                    company.name,
                    base_url,
                )
            return []

        results: list[dict[str, Any]] = []
        async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=REQUEST_TIMEOUT) as client:
            for entry in job_entries:
                job_id = entry["job_id"]
                job_url = entry["url"]
                lastmod = entry["lastmod"]
                try:
                    detail = await self._fetch_detail(client, job_url)
                    results.append(
                        {
                            "id": job_id,
                            "job_id": job_id,
                            "sitemap_url": job_url,
                            "lastmod": lastmod,
                            **detail,
                        }
                    )
                except ConnectorFetchError as exc:
                    if structlog:
                        logger.warning(
                            "icims_detail_fetch_failed",
                            company=company.name,
                            job_id=job_id,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "icims_detail_fetch_failed company=%s job_id=%s error=%s",
                            company.name,
                            job_id,
                            exc,
                        )
                    continue
                except Exception as exc:  # noqa: BLE001
                    if structlog:
                        logger.warning(
                            "icims_detail_unexpected",
                            company=company.name,
                            job_id=job_id,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "icims_detail_unexpected company=%s job_id=%s error=%s",
                            company.name,
                            job_id,
                            exc,
                        )
                    continue
                await asyncio.sleep(self.detail_delay)

        return results

    async def _fetch_sitemap(self, base_url: str) -> list[dict[str, Any]]:
        sitemap_url = f"{base_url}/sitemap.xml"
        async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(sitemap_url)

        if response.status_code in (403, 404, 405):
            if structlog:
                logger.info(
                    "icims_sitemap_unavailable_will_paginate",
                    url=sitemap_url,
                    status_code=response.status_code,
                )
            else:
                logger.info(
                    "icims_sitemap_unavailable_will_paginate url=%s status_code=%s",
                    sitemap_url,
                    response.status_code,
                )
            return await self._fetch_via_pagination(base_url)

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"iCIMS sitemap failed: {response.status_code}",
                response.status_code,
            )

        try:
            root = ET.fromstring(_response_content(response))
        except ET.ParseError as exc:
            raise ParseError(f"iCIMS sitemap XML parse error: {exc}") from exc

        entries: list[dict[str, Any]] = []
        for url_el in root.findall(f"{{{SITEMAP_NS}}}url"):
            loc_el = url_el.find(f"{{{SITEMAP_NS}}}loc")
            lastmod_el = url_el.find(f"{{{SITEMAP_NS}}}lastmod")
            if loc_el is None:
                continue

            loc = loc_el.text or ""
            if not _is_job_detail_url(loc):
                continue

            job_id = _extract_job_id_from_url(loc)
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

    async def _fetch_via_pagination(self, base_url: str) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        page = 0

        async with AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=REQUEST_TIMEOUT) as client:
            while page <= 100:
                url = f"{base_url}/jobs/search?pr={page}&in_iframe=1"
                response = await client.get(url)
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(_response_content(response), "html.parser")
                links = soup.select("a.iCIMS_Anchor[href*='/jobs/']")
                if not links:
                    break

                page_had_new = False
                for link in links:
                    href = link.get("href", "")
                    if not re.search(r"/jobs/\d+/.+/job", href):
                        continue
                    job_id = _extract_job_id_from_url(href)
                    if not job_id or job_id in seen_ids:
                        continue
                    if href.startswith("/"):
                        href = f"{base_url}{href}"
                    seen_ids.add(job_id)
                    entries.append({"job_id": job_id, "url": href, "lastmod": None})
                    page_had_new = True

                if not page_had_new:
                    break

                page += 1
                await asyncio.sleep(self.detail_delay)

        return entries

    async def _fetch_detail(self, client: AsyncSession, job_url: str) -> dict[str, Any]:
        separator = "&" if "?" in job_url else "?"
        detail_url = f"{job_url}{separator}in_iframe=1"
        response = await client.get(detail_url)

        if response.status_code == 429:
            await asyncio.sleep(5.0)
            response = await client.get(detail_url)

        if response.status_code == 404:
            raise ConnectorFetchError(f"iCIMS job 404: {job_url}", 404)

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"iCIMS detail failed {response.status_code}: {job_url}",
                response.status_code,
            )

        parsed = _parse_detail_html(_response_content(response))
        parsed["detail_url"] = detail_url
        return parsed
