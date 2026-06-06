from __future__ import annotations

from typing import Any

import httpx

from app.exceptions import ConnectorFetchError, ParseError
from app.ingestion.connectors.base import BaseConnector
from app.models.company import Company


class LeverConnector(BaseConnector):
    base_url = "https://api.lever.co/v0/postings"

    async def fetch_jobs(self, company: Company) -> list[dict[str, Any]]:
        url = f"{self.base_url}/{company.board_token}"
        params = {"mode": "json"}
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                payload = response.json()
        except Exception as exc:  # noqa: BLE001
            raise ConnectorFetchError(f"Lever fetch failed for {company.board_token}: {exc}") from exc

        if not isinstance(payload, list):
            raise ParseError(f"Malformed Lever response for {company.board_token}")
        return payload
