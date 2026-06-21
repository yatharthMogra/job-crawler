from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TeslaStatePayload(BaseModel):
    state: dict[str, Any] = Field(description="Full /cua-api/apps/careers/state response")


class TeslaPushPayload(BaseModel):
    state: dict[str, Any] = Field(description="Full /cua-api/apps/careers/state response")
    details: list[dict[str, Any]] = Field(default_factory=list)


class TeslaPlanResponse(BaseModel):
    sites: list[str]
    listing_count: int
    known_count: int
    pending_detail_ids: list[str]


class TeslaPushResponse(BaseModel):
    status: str
    run_id: str
    listing_count: int
    new_details_received: int
    jobs_fetched: int
    jobs_new: int
    jobs_updated: int
    jobs_unchanged: int
    jobs_removed: int
