from __future__ import annotations

import asyncio
import json
import re
from typing import Any

import httpx

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company

BUILD_ID_PATTERN = re.compile(r'"buildId":"([^"]+)"')
NEXT_DATA_PATTERN = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>'
)

BASE_URL = "https://ats.rippling.com"
DETAIL_CONCURRENCY = 5
DETAIL_DELAY = 0.3
NEXTJS_HEADER = {"x-nextjs-data": "1"}


class RipplingConnector(BaseConnector):
    failure_alert_threshold = 2
    detail_concurrency = DETAIL_CONCURRENCY
    detail_delay = DETAIL_DELAY

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        slug = self._resolve_slug(company)
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                build_id, first_page_data = await self._fetch_list_page(client, slug)
                summaries = self._extract_job_summaries(first_page_data)

                page = int(first_page_data.get("page", 0))
                total_pages = int(first_page_data.get("totalPages", 1))
                while page + 1 < total_pages:
                    page += 1
                    page_data = await self._fetch_list_json(client, slug, build_id, page)
                    summaries.extend(self._extract_job_summaries(page_data))

                if not summaries:
                    return []

                semaphore = asyncio.Semaphore(self.detail_concurrency)
                tasks = [
                    self._fetch_job_detail(client, slug, build_id, summary, semaphore)
                    for summary in summaries
                ]
                details = await asyncio.gather(*tasks)

            jobs: list[dict[str, Any]] = []
            for summary, detail in zip(summaries, details):
                if detail is None:
                    continue
                jobs.append(self._merge_job(slug, summary, detail))
            return jobs
        except ParseError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(f"Rippling fetch failed for {slug}: {exc}") from exc

    def _resolve_slug(self, company: Company) -> str:
        config = company.platform_config or {}
        return config.get("company_slug") or company.board_token

    async def _fetch_list_page(
        self,
        client: httpx.AsyncClient,
        slug: str,
    ) -> tuple[str, dict[str, Any]]:
        response = await client.get(f"{BASE_URL}/{slug}/jobs")
        response.raise_for_status()
        html = response.text
        build_id = self._extract_build_id(html, slug)
        next_data = self._parse_next_data(html, slug)
        page_data = self._extract_job_posts_query_data(next_data, slug)
        return build_id, page_data

    def _extract_build_id(self, html: str, slug: str) -> str:
        match = BUILD_ID_PATTERN.search(html)
        if not match:
            raise ParseError(f"Missing Rippling buildId for {slug}")
        return match.group(1)

    def _parse_next_data(self, html: str, slug: str) -> dict[str, Any]:
        match = NEXT_DATA_PATTERN.search(html)
        if not match:
            raise ParseError(f"Missing Rippling __NEXT_DATA__ for {slug}")
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise ParseError(f"Malformed Rippling __NEXT_DATA__ for {slug}") from exc
        if not isinstance(data, dict):
            raise ParseError(f"Malformed Rippling __NEXT_DATA__ for {slug}")
        return data

    def _extract_job_posts_query_data(self, next_data: dict[str, Any], slug: str) -> dict[str, Any]:
        page_props = next_data.get("props", {}).get("pageProps", {})
        if not isinstance(page_props, dict):
            raise ParseError(f"Malformed Rippling pageProps for {slug}")
        dehydrated = page_props.get("dehydratedState")
        if not isinstance(dehydrated, dict):
            raise ParseError(f"Malformed Rippling dehydratedState for {slug}")
        queries = dehydrated.get("queries")
        if not isinstance(queries, list) or not queries:
            raise ParseError(f"Malformed Rippling queries for {slug}")
        first_query = queries[0]
        if not isinstance(first_query, dict):
            raise ParseError(f"Malformed Rippling job-posts query for {slug}")
        query_key = first_query.get("queryKey")
        if not isinstance(query_key, list) or len(query_key) < 3 or query_key[2] != "job-posts":
            raise ParseError(f"Malformed Rippling job-posts query for {slug}")
        state = first_query.get("state", {})
        if not isinstance(state, dict):
            raise ParseError(f"Malformed Rippling job-posts state for {slug}")
        data = state.get("data")
        if not isinstance(data, dict):
            raise ParseError(f"Malformed Rippling job-posts data for {slug}")
        return data

    def _extract_job_summaries(self, page_data: dict[str, Any]) -> list[dict[str, Any]]:
        items = page_data.get("items")
        if items is None:
            return []
        if not isinstance(items, list):
            raise ParseError("Malformed Rippling job list items")
        return [item for item in items if isinstance(item, dict) and item.get("id")]

    async def _fetch_list_json(
        self,
        client: httpx.AsyncClient,
        slug: str,
        build_id: str,
        page: int,
    ) -> dict[str, Any]:
        url = f"{BASE_URL}/_next/data/{build_id}/{slug}/jobs.json"
        params = {"page": page} if page > 0 else None
        response = await client.get(url, params=params, headers=NEXTJS_HEADER)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ParseError(f"Malformed Rippling list JSON for {slug} page {page}")
        page_props = payload.get("pageProps", {})
        if not isinstance(page_props, dict):
            raise ParseError(f"Malformed Rippling list JSON for {slug} page {page}")
        dehydrated = page_props.get("dehydratedState", {})
        if not isinstance(dehydrated, dict):
            raise ParseError(f"Malformed Rippling list JSON for {slug} page {page}")
        queries = dehydrated.get("queries", [])
        if not isinstance(queries, list) or not queries:
            raise ParseError(f"Malformed Rippling list JSON for {slug} page {page}")
        first_query = queries[0]
        if not isinstance(first_query, dict):
            raise ParseError(f"Malformed Rippling list JSON for {slug} page {page}")
        state = first_query.get("state", {})
        if not isinstance(state, dict):
            raise ParseError(f"Malformed Rippling list JSON for {slug} page {page}")
        data = state.get("data")
        if not isinstance(data, dict):
            raise ParseError(f"Malformed Rippling list JSON for {slug} page {page}")
        return data

    async def _fetch_job_detail(
        self,
        client: httpx.AsyncClient,
        slug: str,
        build_id: str,
        summary: dict[str, Any],
        semaphore: asyncio.Semaphore,
    ) -> dict[str, Any] | None:
        job_id = summary.get("id")
        if not job_id:
            return None

        url = f"{BASE_URL}/_next/data/{build_id}/{slug}/jobs/{job_id}.json"
        async with semaphore:
            try:
                response = await client.get(url, headers=NEXTJS_HEADER)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                payload = response.json()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                raise ConnectorFetchError(
                    f"Rippling detail failed for {slug}/{job_id}: {exc}"
                ) from exc
            except Exception as exc:  # noqa: BLE001
                raise ConnectorFetchError(
                    f"Rippling detail failed for {slug}/{job_id}: {exc}"
                ) from exc
            finally:
                await asyncio.sleep(self.detail_delay)

        if not isinstance(payload, dict):
            raise ParseError(f"Malformed Rippling detail response for {slug}/{job_id}")
        page_props = payload.get("pageProps", {})
        if not isinstance(page_props, dict):
            raise ParseError(f"Malformed Rippling detail response for {slug}/{job_id}")
        api_data = page_props.get("apiData", {})
        if not isinstance(api_data, dict):
            raise ParseError(f"Malformed Rippling detail response for {slug}/{job_id}")
        job_post = api_data.get("jobPost")
        if not isinstance(job_post, dict):
            raise ParseError(f"Malformed Rippling detail response for {slug}/{job_id}")
        return job_post

    def _merge_job(
        self,
        slug: str,
        summary: dict[str, Any],
        detail: dict[str, Any],
    ) -> dict[str, Any]:
        job_id = str(summary.get("id") or detail.get("uuid"))
        external_link = (
            summary.get("url")
            or detail.get("url")
            or f"{BASE_URL}/{slug}/jobs/{job_id}"
        )
        merged = {**summary, **detail}
        merged["id"] = job_id
        merged["externalLink"] = external_link
        return merged
