from __future__ import annotations

from typing import Any

import httpx

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company


class GreenhouseConnector(BaseConnector):
    base_url = "https://boards-api.greenhouse.io/v1/boards"

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        url = f"{self.base_url}/{company.board_token}/jobs"
        params = {"content": "true"}
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                payload = response.json()
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(
                f"Greenhouse fetch failed for {company.board_token}: {exc}"
            ) from exc

        if not isinstance(payload, dict) or not isinstance(payload.get("jobs"), list):
            raise ParseError(f"Malformed Greenhouse response for {company.board_token}")
        return payload["jobs"]
