from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import httpx

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.config import get_settings
from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.job_freshness import FreshnessVerdict, classify_job
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

DETAIL_DELAY = 0.5
LIST_PAGE_DELAY = 0.5
MAX_PAGE_SIZE = 100

ORACLE_HEADERS = {
    "ora-irc-language": "en",
    "content-type": "application/vnd.oracle.adf.resourceitem+json;charset=utf-8",
}

_LIST_EXPAND = (
    "requisitionList.workLocation,"
    "requisitionList.otherWorkLocations,"
    "requisitionList.secondaryLocations"
)


class OracleHCMConnector(BaseConnector):
    detail_delay = DETAIL_DELAY

    def __init__(self) -> None:
        self._session_user_id = str(uuid.uuid4())

    def _headers(self) -> dict[str, str]:
        return {**ORACLE_HEADERS, "ora-irc-cx-userid": self._session_user_id}

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        datacenter = config.get("datacenter", "us2")
        return (
            f"https://{company.board_token}.fa.{datacenter}.oraclecloud.com"
            f"/hcmRestApi/resources/latest"
        )

    def _site_number(self, company: Company) -> str:
        config = self._platform_config(company)
        return str(config.get("site_number", "CX_1"))

    def _public_posting_url(self, company: Company, job_id: str) -> str:
        config = self._platform_config(company)
        datacenter = config.get("datacenter", "us2")
        site_number = self._site_number(company)
        return (
            f"https://{company.board_token}.fa.{datacenter}.oraclecloud.com"
            f"/hcmUI/CandidateExperience/en/sites/{site_number}"
            f"/requisitions/{job_id}/details"
        )

    def _max_posted_age_days(self, company: Company) -> int:  # noqa: ARG002
        return max(1, get_settings().job_max_age_days)

    @classmethod
    def _job_is_stale(cls, job: dict[str, Any], reference: datetime, max_age_days: int) -> bool:
        return (
            classify_job(job, "oracle_hcm", reference=reference, max_age_days=max_age_days)
            == FreshnessVerdict.STALE
        )

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        base_url = self._base_url(company)
        site_number = self._site_number(company)
        max_posted_age_days = self._max_posted_age_days(company)
        reference = datetime.now(timezone.utc)
        listings = await self._fetch_all_pages(base_url, site_number)
        if not listings:
            return []

        jobs_with_detail: list[dict[str, Any]] = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            for listing in listings:
                job_id = listing.get("Id")
                if not job_id:
                    continue

                list_recency = classify_job(
                    listing, "oracle_hcm", reference=reference, max_age_days=max_posted_age_days
                )
                if list_recency == FreshnessVerdict.STALE:
                    continue

                try:
                    detail = await self._fetch_detail(client, base_url, site_number, str(job_id))
                except ConnectorFetchError as exc:
                    if structlog:
                        logger.warning(
                            "oracle_detail_fetch_failed",
                            company=company.name,
                            job_id=job_id,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "oracle_detail_fetch_failed company=%s job_id=%s error=%s",
                            company.name,
                            job_id,
                            exc,
                        )
                    continue
                except Exception as exc:  # noqa: BLE001
                    if structlog:
                        logger.warning(
                            "oracle_detail_unexpected_error",
                            company=company.name,
                            job_id=job_id,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "oracle_detail_unexpected_error company=%s job_id=%s error=%s",
                            company.name,
                            job_id,
                            exc,
                        )
                    continue

                merged = {**listing, **detail}
                if self._job_is_stale(merged, reference, max_posted_age_days):
                    continue

                merged["id"] = str(job_id)
                merged["externalLink"] = self._public_posting_url(company, str(job_id))
                jobs_with_detail.append(merged)
                await asyncio.sleep(self.detail_delay)

        return jobs_with_detail

    async def _fetch_all_pages(self, base_url: str, site_number: str) -> list[dict[str, Any]]:
        all_jobs: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        offset = 0
        limit = MAX_PAGE_SIZE
        total_count: int | None = None
        url = f"{base_url}/recruitingCEJobRequisitions"

        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                params = {
                    "onlyData": "true",
                    "expand": _LIST_EXPAND,
                    "finder": (
                        f"findReqs;siteNumber={site_number},"
                        f"offset={offset},limit={limit}"
                    ),
                }
                response = await client.get(url, params=params, headers=self._headers())

                if response.status_code in (301, 302):
                    raise ConnectorFetchError(
                        "Oracle HCM redirected — likely SSO-protected"
                    )
                if response.status_code != 200:
                    raise ConnectorFetchError(
                        f"Oracle HCM list failed: HTTP {response.status_code}"
                    )

                try:
                    data = response.json()
                except Exception as exc:  # noqa: BLE001
                    raise ParseError("Oracle HCM list response is not valid JSON") from exc

                items = data.get("items", [])
                if not items:
                    break

                requisition_page = items[0]
                if not isinstance(requisition_page, dict):
                    raise ParseError("Oracle HCM list response missing requisition page")

                jobs_on_page = requisition_page.get("requisitionList", [])
                if not isinstance(jobs_on_page, list):
                    raise ParseError("Oracle HCM list response missing requisitionList array")

                if total_count is None:
                    raw_total = requisition_page.get("TotalJobsCount")
                    if isinstance(raw_total, int) and raw_total > 0:
                        total_count = raw_total
                    elif raw_total is not None:
                        try:
                            parsed_total = int(raw_total)
                            if parsed_total > 0:
                                total_count = parsed_total
                        except (TypeError, ValueError):
                            pass

                if not jobs_on_page:
                    break

                for job in jobs_on_page:
                    if not isinstance(job, dict):
                        continue
                    job_id = job.get("Id")
                    if job_id is not None:
                        job_id_str = str(job_id)
                        if job_id_str in seen_ids:
                            continue
                        seen_ids.add(job_id_str)
                    all_jobs.append(job)

                offset += len(jobs_on_page)

                if total_count is not None:
                    if offset >= total_count:
                        break
                elif len(jobs_on_page) < limit:
                    break

                await asyncio.sleep(LIST_PAGE_DELAY)

        return all_jobs

    async def _fetch_detail(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        site_number: str,
        job_id: str,
    ) -> dict[str, Any]:
        url = f"{base_url}/recruitingCEJobRequisitionDetails"
        params = {
            "expand": "all",
            "onlyData": "true",
            "finder": f'ById;Id="{job_id}",siteNumber={site_number}',
        }
        response = await client.get(url, params=params, headers=self._headers())

        if response.status_code == 429:
            await asyncio.sleep(3.0)
            response = await client.get(url, params=params, headers=self._headers())

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"Oracle HCM detail failed for {job_id}: HTTP {response.status_code}"
            )

        try:
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            raise ParseError(f"Oracle HCM detail response not valid JSON: {job_id}") from exc

        items = data.get("items", [])
        if not items or not isinstance(items[0], dict):
            raise ParseError(f"Oracle HCM detail returned empty items for {job_id}")

        return items[0]
