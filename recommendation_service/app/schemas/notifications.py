from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class DigestFiltersIn(BaseModel):
    locations: list[str] = Field(default_factory=list)
    minimum_salary: Optional[int] = None
    domains: list[str] = Field(default_factory=list)
    employment_type: Optional[Literal["internship", "fulltime"]] = None


class NotificationPreferencesOut(BaseModel):
    candidate_id: uuid.UUID
    digest_enabled: bool
    company_watch_enabled: bool
    cadence_hours: int
    top_k: int
    digest_filters: Optional[dict[str, Any]] = None
    last_digest_sent_at: Optional[datetime] = None
    next_digest_due_at: Optional[datetime] = None


class NotificationPreferencesUpdateIn(BaseModel):
    digest_enabled: Optional[bool] = None
    company_watch_enabled: Optional[bool] = None
    cadence_hours: Optional[int] = None
    top_k: Optional[int] = None
    digest_filters: Optional[DigestFiltersIn] = None


class CompanyWatchItemOut(BaseModel):
    company_id: uuid.UUID
    company_name: str
    platform: str
    is_active: bool


class CompanyWatchListOut(BaseModel):
    candidate_id: uuid.UUID
    companies: list[CompanyWatchItemOut]


class CompanyWatchUpdateIn(BaseModel):
    company_ids: list[uuid.UUID]


class CompanySearchOut(BaseModel):
    id: uuid.UUID
    name: str
    platform: str
    is_active: bool
