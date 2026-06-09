from __future__ import annotations

import asyncio
from typing import Any

import httpx

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company


class AshbyConnector(BaseConnector):
    base_url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
    detail_url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting"
    detail_concurrency = 3
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

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        listings = await self._fetch_listings(company)
        if not listings:
            return []

        semaphore = asyncio.Semaphore(self.detail_concurrency)
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = [
                self._fetch_posting_detail(client, company.board_token, listing, semaphore)
                for listing in listings
            ]
            details = await asyncio.gather(*tasks)

        normalized_postings: list[dict[str, Any]] = []
        for listing, detail in zip(listings, details, strict=True):
            job_id = listing.get("id")
            if not job_id:
                continue
            merged = {**listing, **(detail or {})}
            normalized_postings.append(
                {
                    **merged,
                    "externalLink": f"https://jobs.ashbyhq.com/{company.board_token}/{job_id}",
                }
            )
        return normalized_postings

    async def _fetch_listings(self, company: Company) -> list[dict[str, Any]]:
        request_payload = {
            "operationName": "ApiJobBoardWithTeams",
            "variables": {"organizationHostedJobsPageName": company.board_token},
            "query": self._LIST_QUERY,
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.base_url, json=request_payload)
                response.raise_for_status()
                payload = response.json()
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(f"Ashby fetch failed for {company.board_token}: {exc}") from exc

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
    ) -> dict[str, Any]:
        job_id = str(listing["id"])
        request_payload = {
            "operationName": "ApiJobPosting",
            "variables": {
                "organizationHostedJobsPageName": board_token,
                "jobPostingId": job_id,
            },
            "query": self._DETAIL_QUERY,
        }
        payload: dict[str, Any] | None = None
        last_error: Exception | None = None
        async with semaphore:
            for attempt in range(self.detail_retry_attempts):
                try:
                    response = await client.post(self.detail_url, json=request_payload)
                    if response.status_code == 429:
                        await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
                        continue
                    response.raise_for_status()
                    payload = response.json()
                    break
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    if attempt + 1 >= self.detail_retry_attempts:
                        break
                    await asyncio.sleep(self.detail_retry_base_seconds * (2**attempt))
            await asyncio.sleep(0.15)

        if payload is None:
            raise ConnectorFetchError(
                f"Ashby detail fetch failed for {board_token}/{job_id}: {last_error}"
            ) from last_error

        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            first_error = errors[0]
            message = first_error.get("message") if isinstance(first_error, dict) else str(first_error)
            raise ParseError(f"Ashby detail API returned errors for {board_token}/{job_id}: {message}")

        job_posting = payload.get("data", {}).get("jobPosting") if isinstance(payload, dict) else None
        if not isinstance(job_posting, dict):
            raise ParseError(f"Malformed Ashby detail response for {board_token}/{job_id}")
        return job_posting
