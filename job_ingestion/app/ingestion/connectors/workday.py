from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
from datetime import date, datetime, timezone
from typing import Any, Literal, Optional

import httpx

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.config import get_settings
from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.job_freshness import FreshnessVerdict, classify_job, workday_listing_recency_hint
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)

MAX_PAGE_SIZE = 20
DEFAULT_WORKDAY_FULL_REFRESH_DAYS = 7
_JOB_REQ_ID_SUFFIX = re.compile(r"_([^/_]+)$")
_CONSECUTIVE_STALE_PAGES_TO_STOP = 2


class WorkdayConnector(BaseConnector):
    detail_concurrency = 1
    detail_retry_attempts = 5
    detail_retry_base_seconds = 2.0
    detail_delay = 0.35

    async def fetch_jobs(
        self,
        company: Company,
        *,
        known_raw_by_id: dict[str, dict[str, Any]] | None = None,
        known_raw_fetched_at: dict[str, datetime] | None = None,
    ) -> list[dict[str, Any]]:
        base_url = self._base_url(company)
        public_base_url = self._public_base_url(company)
        max_posted_age_days = self._max_posted_age_days(company)
        reference = datetime.now(timezone.utc)
        reference_date = reference.date()
        fetch_mode = self._workday_fetch_mode(company)
        full_refresh_days = self._workday_full_refresh_days(company)
        cached_raw = known_raw_by_id or {}
        cached_fetched_at = known_raw_fetched_at or {}
        listings = await self._fetch_all_pages(
            base_url, company, max_posted_age_days, reference
        )
        if not listings:
            return []

        jobs_with_detail: list[dict[str, Any]] = []
        detail_fetched = 0
        cache_reused = 0
        semaphore = asyncio.Semaphore(self.detail_concurrency)
        async with httpx.AsyncClient(timeout=30.0) as client:
            for listing in listings:
                external_path = listing.get("externalPath")
                job_req_id = self._resolve_job_req_id(listing)
                if not external_path or not job_req_id:
                    continue

                list_recency = workday_listing_recency_hint(
                    listing.get("postedOn"), reference, max_posted_age_days
                )
                if list_recency is False:
                    continue

                cached = cached_raw.get(job_req_id)
                if fetch_mode == "incremental" and cached is not None:
                    if not self._needs_detail_fetch(
                        listing,
                        cached,
                        cached_fetched_at.get(job_req_id),
                        reference_date,
                        full_refresh_days,
                    ):
                        job = dict(cached)
                        job["id"] = str(job_req_id)
                        job["externalLink"] = self._public_posting_url(
                            company, public_base_url, str(external_path)
                        )
                        if self._job_is_stale(job, reference, max_posted_age_days):
                            continue
                        jobs_with_detail.append(job)
                        cache_reused += 1
                        continue

                detail_payload: dict[str, Any] | None = None
                try:
                    detail_payload = await self._fetch_detail(
                        client, base_url, str(external_path), semaphore
                    )
                    detail_fetched += 1
                except Exception as exc:  # noqa: BLE001
                    if structlog:
                        logger.warning(
                            "workday_detail_fetch_failed",
                            company=company.name,
                            external_path=external_path,
                            error=str(exc),
                        )
                    else:
                        logger.warning(
                            "workday_detail_fetch_failed company=%s external_path=%s error=%s",
                            company.name,
                            external_path,
                            exc,
                        )

                if detail_payload is not None:
                    job_posting_info = detail_payload.get("jobPostingInfo", {})
                    if not isinstance(job_posting_info, dict):
                        job_posting_info = {}
                    merged = {**listing, **detail_payload, "jobPostingInfo": job_posting_info}
                else:
                    merged = {**listing, "jobPostingInfo": {}}

                if self._job_is_stale(merged, reference, max_posted_age_days):
                    continue

                merged["id"] = str(job_req_id)
                merged["externalLink"] = self._public_posting_url(
                    company, public_base_url, str(external_path)
                )
                jobs_with_detail.append(merged)
                await asyncio.sleep(self.detail_delay)

        if fetch_mode == "incremental" and structlog:
            logger.info(
                "workday_incremental_fetch_complete",
                company=company.name,
                detail_fetched=detail_fetched,
                cache_reused=cache_reused,
                total=len(jobs_with_detail),
            )
        elif fetch_mode == "incremental":
            logger.info(
                "workday_incremental_fetch_complete company=%s detail_fetched=%s "
                "cache_reused=%s total=%s",
                company.name,
                detail_fetched,
                cache_reused,
                len(jobs_with_detail),
            )

        return jobs_with_detail

    def _workday_fetch_mode(self, company: Company) -> Literal["full", "incremental"]:
        config = self._platform_config(company)
        mode = str(config.get("workday_fetch_mode", "full")).strip().lower()
        if mode == "incremental":
            return "incremental"
        return "full"

    def _workday_full_refresh_days(self, company: Company) -> int:
        config = self._platform_config(company)
        value = config.get("workday_full_refresh_days", DEFAULT_WORKDAY_FULL_REFRESH_DAYS)
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return DEFAULT_WORKDAY_FULL_REFRESH_DAYS

    @staticmethod
    def _listing_fingerprint(listing: dict[str, Any]) -> str:
        payload = {
            "title": listing.get("title"),
            "locationsText": listing.get("locationsText"),
            "externalPath": listing.get("externalPath"),
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @classmethod
    def _cached_listing_fingerprint(cls, cached: dict[str, Any]) -> str:
        return cls._listing_fingerprint(cached)

    @classmethod
    def _has_job_description(cls, cached: dict[str, Any]) -> bool:
        info = cached.get("jobPostingInfo")
        if not isinstance(info, dict):
            return False
        description = info.get("jobDescription")
        return isinstance(description, str) and bool(description.strip())

    @classmethod
    def _needs_detail_fetch(
        cls,
        listing: dict[str, Any],
        cached: dict[str, Any],
        cached_fetched_at: datetime | None,
        reference_date: date,
        full_refresh_days: int,
    ) -> bool:
        if cls._listing_fingerprint(listing) != cls._cached_listing_fingerprint(cached):
            return True
        if not cls._has_job_description(cached):
            return True
        if cached_fetched_at is not None:
            fetched_date = cached_fetched_at
            if fetched_date.tzinfo is None:
                fetched_date = fetched_date.replace(tzinfo=timezone.utc)
            age_days = (reference_date - fetched_date.date()).days
            if age_days >= full_refresh_days:
                return True
        return False

    def _max_posted_age_days(self, company: Company) -> int:  # noqa: ARG002
        return max(1, get_settings().job_max_age_days)

    def _stop_pagination_on_stale_tail(self, company: Company) -> bool:
        config = self._platform_config(company)
        value = config.get("stop_pagination_on_stale_tail", False)
        return bool(value)

    def _tenant(self, company: Company) -> str:
        config = self._platform_config(company)
        tenant = config.get("tenant")
        if tenant:
            return str(tenant)
        return company.board_token

    @staticmethod
    def _job_is_stale(job: dict[str, Any], reference: datetime, max_age_days: int) -> bool:
        return (
            classify_job(job, "workday", reference=reference, max_age_days=max_age_days)
            == FreshnessVerdict.STALE
        )

    @staticmethod
    def _resolve_job_req_id(listing: dict[str, Any]) -> str | None:
        job_req_id = listing.get("jobReqId")
        if job_req_id:
            return str(job_req_id)

        bullet_fields = listing.get("bulletFields")
        if isinstance(bullet_fields, list):
            for bullet in bullet_fields:
                if bullet:
                    return str(bullet)

        external_path = listing.get("externalPath")
        if isinstance(external_path, str):
            match = _JOB_REQ_ID_SUFFIX.search(external_path)
            if match:
                return match.group(1)
        return None

    def _platform_config(self, company: Company) -> dict[str, Any]:
        config = company.platform_config
        return config if isinstance(config, dict) else {}

    def _base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        instance = config.get("instance", "wd1")
        career_site = config.get("career_site", "External")
        tenant = self._tenant(company)
        return (
            f"https://{tenant}.{instance}.myworkdayjobs.com"
            f"/wday/cxs/{tenant}/{career_site}"
        )

    def _public_base_url(self, company: Company) -> str:
        config = self._platform_config(company)
        instance = config.get("instance", "wd1")
        tenant = self._tenant(company)
        return f"https://{tenant}.{instance}.myworkdayjobs.com"

    def _public_posting_url(
        self,
        company: Company,
        public_base_url: str,
        external_path: str,
    ) -> str:
        config = self._platform_config(company)
        prefix = str(config.get("public_path_prefix") or config.get("career_site") or "").strip("/")
        if prefix:
            if external_path.startswith("/job/"):
                return f"{public_base_url}/{prefix}{external_path}"
            return f"{public_base_url}/{prefix}/job{external_path}"
        if external_path.startswith("/job/"):
            return f"{public_base_url}{external_path}"
        return f"{public_base_url}/job{external_path}"

    @staticmethod
    def _detail_url(base_url: str, external_path: str) -> str:
        if external_path.startswith("/job/"):
            return f"{base_url}{external_path}"
        return f"{base_url}/job{external_path}"

    async def _fetch_all_pages(
        self,
        base_url: str,
        company: Company,
        max_posted_age_days: int,
        reference: datetime,
    ) -> list[dict[str, Any]]:
        all_jobs: list[dict[str, Any]] = []
        offset = 0
        stop_on_stale_tail = self._stop_pagination_on_stale_tail(company)
        seen_fresh_page = False
        consecutive_stale_pages = 0

        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                response: httpx.Response | None = None
                last_error: Exception | None = None
                for attempt in range(self.detail_retry_attempts):
                    try:
                        response = await client.post(
                            f"{base_url}/jobs",
                            json={
                                "appliedFacets": {},
                                "limit": MAX_PAGE_SIZE,
                                "offset": offset,
                                "searchText": "",
                            },
                        )
                        if response.status_code in (429, 502, 503):
                            await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
                            continue
                        if response.status_code != 200:
                            raise ConnectorFetchError(
                                f"Workday list failed for {base_url}: HTTP {response.status_code}"
                            )
                        break
                    except ConnectorFetchError:
                        raise
                    except Exception as exc:  # noqa: BLE001
                        last_error = exc
                        if attempt + 1 >= self.detail_retry_attempts:
                            break
                        await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))

                if response is None or response.status_code != 200:
                    raise ConnectorFetchError(
                        f"Workday list fetch failed for {base_url}: {last_error}"
                    ) from last_error

                try:
                    data = response.json()
                except Exception as exc:  # noqa: BLE001
                    raise ParseError(
                        f"Workday list response is not valid JSON for {base_url}"
                    ) from exc

                postings = data.get("jobPostings")
                if not isinstance(postings, list):
                    raise ParseError(
                        f"Workday list response missing jobPostings array for {base_url}"
                    )

                page_hints: list[Optional[bool]] = []
                for posting in postings:
                    if not isinstance(posting, dict):
                        continue
                    hint = workday_listing_recency_hint(
                        posting.get("postedOn"), reference, max_posted_age_days
                    )
                    page_hints.append(hint)
                    if hint is not False:
                        all_jobs.append(posting)

                if not postings:
                    break

                if stop_on_stale_tail and page_hints:
                    if any(hint is True for hint in page_hints):
                        seen_fresh_page = True
                    if all(hint is False for hint in page_hints):
                        if seen_fresh_page:
                            consecutive_stale_pages += 1
                        if consecutive_stale_pages >= _CONSECUTIVE_STALE_PAGES_TO_STOP:
                            break
                    else:
                        consecutive_stale_pages = 0

                offset += MAX_PAGE_SIZE
                total = data.get("total")
                if isinstance(total, int) and offset >= total:
                    break

        return all_jobs

    async def _fetch_detail(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        external_path: str,
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any]:
        url = self._detail_url(base_url, external_path)
        payload: dict[str, Any] | None = None
        last_error: Exception | None = None

        async with semaphore:
            for attempt in range(self.detail_retry_attempts):
                try:
                    response = await client.get(url)
                    if response.status_code in (429, 503):
                        await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
                        continue
                    if response.status_code != 200:
                        raise ConnectorFetchError(
                            f"Workday detail failed for {external_path}: HTTP {response.status_code}"
                        )
                    try:
                        payload = response.json()
                    except Exception as exc:  # noqa: BLE001
                        raise ParseError(
                            f"Workday detail response is not valid JSON: {external_path}"
                        ) from exc
                    break
                except (ConnectorFetchError, ParseError):
                    raise
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    if attempt + 1 >= self.detail_retry_attempts:
                        break
                    await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))

        if payload is None:
            raise ConnectorFetchError(
                f"Workday detail fetch failed for {external_path}: {last_error}"
            ) from last_error

        if not isinstance(payload, dict):
            raise ParseError(f"Malformed Workday detail response for {external_path}")
        return payload
