from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.enrichment import JobEnrichmentOut


class NormalizedJobOut(BaseModel):
    id: str
    external_job_id: str
    title: str
    company_name: str
    location: Optional[str]
    department: Optional[str]
    posting_url: Optional[str]
    description_preview: Optional[str]
    is_active: bool
    processing_state: str
    failure_reason: Optional[str]
    last_seen_at: datetime
    last_manual_review_at: Optional[datetime]
    extracted_at: datetime


class NormalizedJobDetailOut(NormalizedJobOut):
    company_id: str
    raw_job_id: str
    external_job_id: str
    employment_type: Optional[str]
    posted_at: Optional[datetime]
    consecutive_misses: int
    last_seen_at: datetime
    extraction_version: str
    llm_provider: Optional[str]
    llm_model: Optional[str]
    description_text: Optional[str]
    enrichments: list[JobEnrichmentOut]


class JobReviewPatchIn(BaseModel):
    seniority: Optional[str] = None
    is_internship: Optional[bool] = None
    is_new_grad: Optional[bool] = None
    sponsorship_status: Optional[str] = None
    sponsorship_confidence: Optional[str] = None
    remote_type: Optional[str] = None
    tech_stack: Optional[list[str]] = None
    skills: Optional[list[str]] = None
    comment: str = Field(min_length=1)


class JobFlagIn(BaseModel):
    comment: str = Field(min_length=1)
