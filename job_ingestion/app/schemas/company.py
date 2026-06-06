from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class CompanyOut(BaseModel):
    id: str
    name: str
    platform: str
    board_token: str
    platform_config: Optional[dict[str, Any]] = None
    is_active: bool
    requires_review: bool
    active_jobs_count: Optional[int] = None
    consecutive_fetch_failures: int
    last_failure_at: Optional[datetime]
    flagged_for_review_at: Optional[datetime]
    last_successful_fetch_at: Optional[datetime]


class CompanyPatchIn(BaseModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    board_token: Optional[str] = None
    platform_config: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None


class CompanyFlagIn(BaseModel):
    comment: Optional[str] = None


class CompanySyncOut(BaseModel):
    inserted: int
    updated: int
    deleted: int
