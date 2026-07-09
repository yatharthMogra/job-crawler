from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserApplicationOut(BaseModel):
    id: UUID
    candidate_id: UUID
    job_archive_id: Optional[UUID] = None
    normalized_job_id: Optional[UUID] = None
    company_name: str
    job_title: str
    location: Optional[str] = None
    platform: Optional[str] = None
    external_job_id: Optional[str] = None
    posting_url: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    seniority: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    tech_stack: list[str] = Field(default_factory=list)
    description_text: Optional[str] = None
    logo_url: Optional[str] = None
    applied_at: datetime
    status: str
    notes: Optional[str] = None


class UserApplicationsResponse(BaseModel):
    applications: list[UserApplicationOut]
    total: int


class UserApplicationPatchIn(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
