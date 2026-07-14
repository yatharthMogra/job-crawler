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


class TierEntitlementsOut(BaseModel):
    max_companies: int
    cadence_min_minutes: int
    cadence_max_minutes: int
    delivery: Literal["batched", "instant"]
    max_emails_per_day_cap: int
    default_max_emails_per_day: int
    ats_fit: bool = False
    hiring_manager: bool = False
    apply_agent: bool = False


class NotificationPreferencesOut(BaseModel):
    candidate_id: uuid.UUID
    digest_enabled: bool
    company_watch_enabled: bool
    cadence_hours: int
    top_k: int
    digest_filters: Optional[dict[str, Any]] = None
    last_digest_sent_at: Optional[datetime] = None
    next_digest_due_at: Optional[datetime] = None
    company_watch_cadence_minutes: int
    max_emails_per_day: int
    last_company_watch_batch_at: Optional[datetime] = None
    next_company_watch_due_at: Optional[datetime] = None
    plan_tier: str
    entitlements: TierEntitlementsOut
    emails_sent_today: int


class NotificationPreferencesUpdateIn(BaseModel):
    digest_enabled: Optional[bool] = None
    company_watch_enabled: Optional[bool] = None
    cadence_hours: Optional[int] = None
    top_k: Optional[int] = None
    digest_filters: Optional[DigestFiltersIn] = None
    company_watch_cadence_minutes: Optional[int] = None
    max_emails_per_day: Optional[int] = None


class CompanyWatchItemOut(BaseModel):
    company_id: uuid.UUID
    company_name: str
    platform: str
    is_active: bool


class CompanyWatchListOut(BaseModel):
    candidate_id: uuid.UUID
    companies: list[CompanyWatchItemOut]
    plan_tier: str
    max_companies: int


class CompanyWatchUpdateIn(BaseModel):
    company_ids: list[uuid.UUID]


class CompanySearchOut(BaseModel):
    id: uuid.UUID
    name: str
    platform: str
    is_active: bool
