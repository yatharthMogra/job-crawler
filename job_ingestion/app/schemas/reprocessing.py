from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ReprocessingFilters(BaseModel):
    processing_state: list[str] = Field(default_factory=list)
    extraction_version: Optional[str] = None
    company_id: Optional[str] = None
    platform: Optional[str] = None


class ReprocessingRequest(BaseModel):
    filters: ReprocessingFilters = Field(default_factory=ReprocessingFilters)
    target_version: str = "v2"
    dry_run: bool = True


class ReprocessingResponse(BaseModel):
    matched_jobs: int
    processed_jobs: int
    success_count: int
    failed_count: int
    dry_run: bool
