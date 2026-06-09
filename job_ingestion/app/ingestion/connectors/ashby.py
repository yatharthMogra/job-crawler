from __future__ import annotations

from typing import Any

import httpx

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company


class AshbyConnector(BaseConnector):
    base_url = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"

    _QUERY = """
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

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        payload: dict[str, Any]
        request_payload = {
            "operationName": "ApiJobBoardWithTeams",
            "variables": {"organizationHostedJobsPageName": company.board_token},
            "query": self._QUERY,
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

        normalized_postings: list[dict[str, Any]] = []
        for job in job_postings:
            if not isinstance(job, dict):
                continue
            job_id = job.get("id")
            if not job_id:
                continue
            normalized_postings.append(
                {
                    **job,
                    # Public Ashby URL pattern for a specific job posting.
                    "externalLink": f"https://jobs.ashbyhq.com/{company.board_token}/{job_id}",
                }
            )
        return normalized_postings
