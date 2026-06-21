from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from datetime import date, datetime, timezone
from typing import Any

import httpx

try:
    import structlog
except ImportError:  # pragma: no cover
    structlog = None

from app.config import get_settings
from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.rate_limiter import get_ashby_bucket, parse_retry_after
from app.models.company import Company

logger = structlog.get_logger(__name__) if structlog else logging.getLogger(__name__)


class AshbyConnector(BaseConnector):
    base_url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
    detail_url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting"
    detail_concurrency = 1
    detail_retry_attempts = 5
    detail_retry_base_seconds = 2.0

    _LIST_QUERY = """
query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
  jobBoard: jobBoardWithTeams(
    organizationHostedJobsPageName: $organizationHostedJobsPageName
  ) {
    jobPostings {
      id
      title
      locationName
      employmentType
      secondaryLocations {
        locationName
      }
    }
  }
}
""".strip()

    _DETAIL_QUERY = """
query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {
  jobPosting(
    organizationHostedJobsPageName: $organizationHostedJobsPageName
    jobPostingId: $jobPostingId
  ) {
    id
    title
    locationName
    employmentType
    descriptionHtml
    publishedDate
    departmentName
    secondaryLocationNames
  }
}
""".strip()

    async def fetch_jobs(
        self,
        company: Company,
        *,
        known_raw_by_id: dict[str, dict[str, Any]] | None = None,
        known_raw_fetched_at: dict[str, datetime] | None = None,
    ) -> list[dict[str, Any]]:
        cached_raw = known_raw_by_id or {}
        cached_fetched_at = known_raw_fetched_at or {}
        full_refresh_days = max(1, get_settings().ashby_full_refresh_days)
        reference_date = datetime.now(timezone.utc).date()

        async with httpx.AsyncClient(timeout=30.0) as client:
            listings = await self._fetch_listings(client, company)
            if not listings:
                return []

            normalized_postings: list[dict[str, Any]] = []
            failed_listings: list[dict[str, Any]] = []
            detail_fetched = 0
            cache_reused = 0
            cache_fallback_count = 0
            semaphore = asyncio.Semaphore(self.detail_concurrency)

            for listing in listings:
                job_id = listing.get("id")
                if not job_id:
                    continue
                job_id_str = str(job_id)
                cached = cached_raw.get(job_id_str)

                if cached is not None and not self._needs_detail_fetch(
                    listing,
                    cached,
                    cached_fetched_at.get(job_id_str),
                    reference_date,
                    full_refresh_days,
                ):
                    merged = {**listing, **cached}
                    normalized_postings.append(
                        self._normalize_posting(company.board_token, job_id_str, merged)
                    )
                    cache_reused += 1
                    continue

                detail = await self._fetch_posting_detail(
                    client,
                    company.board_token,
                    listing,
                    semaphore,
                )
                if detail is not None:
                    merged = {**listing, **detail}
                    normalized_postings.append(
                        self._normalize_posting(company.board_token, job_id_str, merged)
                    )
                    detail_fetched += 1
                    continue

                if cached is not None:
                    merged = {**listing, **cached}
                    normalized_postings.append(
                        self._normalize_posting(company.board_token, job_id_str, merged)
                    )
                    cache_fallback_count += 1
                    self._log_detail_fetch_failed(
                        company.board_token,
                        job_id_str,
                        used_cache=True,
                    )
                    continue

                failed_listings.append(listing)
                merged = {**listing}
                normalized_postings.append(
                    self._normalize_posting(company.board_token, job_id_str, merged)
                )
                self._log_detail_fetch_failed(
                    company.board_token,
                    job_id_str,
                    used_cache=False,
                )

            second_pass_recovered = 0
            if failed_listings:
                for listing in failed_listings:
                    job_id = listing.get("id")
                    if not job_id:
                        continue
                    job_id_str = str(job_id)
                    detail = await self._fetch_posting_detail(
                        client,
                        company.board_token,
                        listing,
                        semaphore,
                    )
                    if detail is None:
                        continue
                    merged = {**listing, **detail}
                    for index, posting in enumerate(normalized_postings):
                        if str(posting.get("id")) == job_id_str:
                            normalized_postings[index] = self._normalize_posting(
                                company.board_token,
                                job_id_str,
                                merged,
                            )
                            second_pass_recovered += 1
                            detail_fetched += 1
                            break

            partial_failures = cache_fallback_count + len(failed_listings) - second_pass_recovered
            if partial_failures > 0:
                self._log_partial_detail_failure(
                    board_token=company.board_token,
                    failed_count=partial_failures,
                    total=len(listings),
                    cache_fallback_count=cache_fallback_count,
                    second_pass_recovered=second_pass_recovered,
                )

            if detail_fetched == 0 and cache_reused == 0 and cache_fallback_count == 0:
                raise ConnectorFetchError(
                    f"Ashby detail fetch failed for all jobs on {company.board_token}"
                )

            self._log_incremental_complete(
                board_token=company.board_token,
                detail_fetched=detail_fetched,
                cache_reused=cache_reused,
                total=len(normalized_postings),
            )

        return normalized_postings

    @staticmethod
    def _normalize_posting(
        board_token: str,
        job_id: str,
        merged: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            **merged,
            "id": job_id,
            "externalLink": f"https://jobs.ashbyhq.com/{board_token}/{job_id}",
        }

    @staticmethod
    def _listing_fingerprint(listing: dict[str, Any]) -> str:
        secondary = listing.get("secondaryLocations")
        if isinstance(secondary, list):
            secondary_locations = [
                loc.get("locationName")
                for loc in secondary
                if isinstance(loc, dict) and loc.get("locationName")
            ]
        else:
            secondary_names = listing.get("secondaryLocationNames")
            secondary_locations = secondary_names if isinstance(secondary_names, list) else []

        payload = {
            "title": listing.get("title"),
            "locationName": listing.get("locationName"),
            "employmentType": listing.get("employmentType"),
            "secondaryLocations": secondary_locations,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @classmethod
    def _cached_listing_fingerprint(cls, cached: dict[str, Any]) -> str:
        return cls._listing_fingerprint(cached)

    @staticmethod
    def _has_job_description(cached: dict[str, Any]) -> bool:
        description = cached.get("descriptionHtml")
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

    async def _fetch_listings(
        self,
        client: httpx.AsyncClient,
        company: Company,
    ) -> list[dict[str, Any]]:
        request_payload = {
            "operationName": "ApiJobBoardWithTeams",
            "variables": {"organizationHostedJobsPageName": company.board_token},
            "query": self._LIST_QUERY,
        }
        payload = await self._post_graphql(
            client,
            self.base_url,
            request_payload,
            context=f"Ashby list fetch for {company.board_token}",
        )

        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            first_error = errors[0]
            message = first_error.get("message") if isinstance(first_error, dict) else str(first_error)
            raise ParseError(f"Ashby API returned errors for {company.board_token}: {message}")

        job_board = payload.get("data", {}).get("jobBoard") if isinstance(payload, dict) else None
        job_postings = job_board.get("jobPostings") if isinstance(job_board, dict) else None
        if not isinstance(job_postings, list):
            raise ParseError(f"Malformed Ashby response for {company.board_token}")

        return [job for job in job_postings if isinstance(job, dict) and job.get("id")]

    async def _fetch_posting_detail(
        self,
        client: httpx.AsyncClient,
        board_token: str,
        listing: dict[str, Any],
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any] | None:
        job_id = str(listing["id"])
        request_payload = {
            "operationName": "ApiJobPosting",
            "variables": {
                "organizationHostedJobsPageName": board_token,
                "jobPostingId": job_id,
            },
            "query": self._DETAIL_QUERY,
        }
        async with semaphore:
            try:
                payload = await self._post_graphql(
                    client,
                    self.detail_url,
                    request_payload,
                    context=f"Ashby detail fetch for {board_token}/{job_id}",
                )
            except ConnectorFetchError:
                return None

        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            first_error = errors[0]
            message = first_error.get("message") if isinstance(first_error, dict) else str(first_error)
            raise ParseError(f"Ashby detail API returned errors for {board_token}/{job_id}: {message}")

        job_posting = payload.get("data", {}).get("jobPosting") if isinstance(payload, dict) else None
        if not isinstance(job_posting, dict):
            raise ParseError(f"Malformed Ashby detail response for {board_token}/{job_id}")
        return job_posting

    async def _post_graphql(
        self,
        client: httpx.AsyncClient,
        url: str,
        payload: dict[str, Any],
        *,
        context: str,
    ) -> dict[str, Any]:
        bucket = get_ashby_bucket()
        last_error: Exception | None = None
        for attempt in range(self.detail_retry_attempts):
            try:
                await bucket.acquire()
                response = await client.post(url, json=payload)
                if response.status_code == 429:
                    retry_after = parse_retry_after(response.headers.get("Retry-After"))
                    if retry_after is not None:
                        await asyncio.sleep(retry_after)
                    else:
                        await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
                    continue
                response.raise_for_status()
                body = response.json()
                if not isinstance(body, dict):
                    raise ParseError(f"Malformed Ashby response for {context}")
                return body
            except ParseError:
                raise
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt + 1 >= self.detail_retry_attempts:
                    break
                await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))

        raise ConnectorFetchError(f"{context}: {last_error}") from last_error

    @staticmethod
    def _log_detail_fetch_failed(board_token: str, job_id: str, *, used_cache: bool) -> None:
        if structlog:
            logger.warning(
                "ashby_detail_fetch_failed",
                board_token=board_token,
                job_id=job_id,
                used_cache=used_cache,
            )
        else:
            logger.warning(
                "ashby_detail_fetch_failed board_token=%s job_id=%s used_cache=%s",
                board_token,
                job_id,
                used_cache,
            )

    @staticmethod
    def _log_partial_detail_failure(
        *,
        board_token: str,
        failed_count: int,
        total: int,
        cache_fallback_count: int,
        second_pass_recovered: int,
    ) -> None:
        if structlog:
            logger.warning(
                "ashby_partial_detail_failure",
                board_token=board_token,
                failed_count=failed_count,
                total=total,
                cache_fallback_count=cache_fallback_count,
                second_pass_recovered=second_pass_recovered,
            )
        else:
            logger.warning(
                "ashby_partial_detail_failure board_token=%s failed_count=%s total=%s "
                "cache_fallback_count=%s second_pass_recovered=%s",
                board_token,
                failed_count,
                total,
                cache_fallback_count,
                second_pass_recovered,
            )

    @staticmethod
    def _log_incremental_complete(
        *,
        board_token: str,
        detail_fetched: int,
        cache_reused: int,
        total: int,
    ) -> None:
        if structlog:
            logger.info(
                "ashby_incremental_fetch_complete",
                board_token=board_token,
                detail_fetched=detail_fetched,
                cache_reused=cache_reused,
                total=total,
            )
        else:
            logger.info(
                "ashby_incremental_fetch_complete board_token=%s detail_fetched=%s "
                "cache_reused=%s total=%s",
                board_token,
                detail_fetched,
                cache_reused,
                total,
            )
