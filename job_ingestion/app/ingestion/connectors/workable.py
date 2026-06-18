from __future__ import annotations

from typing import Any

import httpx

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company


def _location_key(location: dict[str, Any]) -> tuple[Any, ...]:
    return (
        location.get("country"),
        location.get("countryCode"),
        location.get("city"),
        location.get("region"),
    )


def _merge_workable_jobs(
    jobs_by_shortcode: dict[str, dict[str, Any]],
    raw: dict[str, Any],
    shortcode: str,
) -> None:
    if shortcode not in jobs_by_shortcode:
        jobs_by_shortcode[shortcode] = {**raw, "id": shortcode}
        return

    existing = jobs_by_shortcode[shortcode]
    existing_locations = existing.setdefault("locations", [])
    seen = {_location_key(loc) for loc in existing_locations if isinstance(loc, dict)}
    for loc in raw.get("locations") or []:
        if not isinstance(loc, dict):
            continue
        key = _location_key(loc)
        if key not in seen:
            existing_locations.append(loc)
            seen.add(key)


class WorkableConnector(BaseConnector):
    base_url = "https://apply.workable.com/api/v1/widget/accounts"

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        url = f"{self.base_url}/{company.board_token}"
        params = {"details": "true"}
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                payload = response.json()
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Workable fetch failed for {company.board_token}: {exc}"
            ) from exc

        if not isinstance(payload, dict) or not isinstance(payload.get("jobs"), list):
            raise ParseError(f"Malformed Workable response for {company.board_token}")

        jobs_by_shortcode: dict[str, dict[str, Any]] = {}
        for raw in payload["jobs"]:
            if not isinstance(raw, dict):
                continue
            shortcode = raw.get("shortcode")
            if not shortcode:
                continue
            _merge_workable_jobs(jobs_by_shortcode, raw, str(shortcode))

        return list(jobs_by_shortcode.values())
