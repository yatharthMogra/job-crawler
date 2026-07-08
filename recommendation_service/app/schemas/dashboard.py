from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class H1BSponsorshipInfo(BaseModel):
    pool_family: str
    total_lca_3yr: int
    approval_rate_3yr: float | None
    is_top_sponsor: bool
    years_covered: list[int]


class CompanyEnrichmentOut(BaseModel):
    founded_year: int | None = None
    headquarters: str | None = None
    employee_count_range: str | None = None
    one_line_description: str | None = None
    website: str | None = None
    linkedin_url: str | None = None
    glassdoor_rating: float | None = None
    logo_url: str | None = None


class DashboardJobOut(BaseModel):
    id: uuid.UUID
    title: str
    company_name: str
    location: Optional[str]
    posting_url: Optional[str]
    description_text: Optional[str] = None
    description_preview: Optional[str] = None
    posted_at: Optional[datetime]
    remote_type: str
    application_effort: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    opportunity_score: Optional[float]
    retrieval_pools: list[str]
    normalized_roles: list[str]
    job_capabilities: list[str]
    tech_stack: list[str]
    skills: list[str]
    seniority: str
    experience_tier: str = "UNKNOWN"
    responsibilities: list[str] = Field(default_factory=list)
    required_qualifications: list[str] = Field(default_factory=list)
    preferred_qualifications: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    sponsorship_status: str = "unclear"
    sponsorship_confidence: str = "low"
    requires_clearance: bool = False
    requires_citizenship: bool = False
    h1b_sponsorship: H1BSponsorshipInfo | None = None
    company_info: CompanyEnrichmentOut | None = None


class DashboardRecommendedJobOut(DashboardJobOut):
    personal_score: float
    match_reasons: list[str] = Field(default_factory=list)


class DashboardJobsResponse(BaseModel):
    jobs: list[DashboardJobOut]
    total: int


class DashboardRecommendedJobsResponse(BaseModel):
    jobs: list[DashboardRecommendedJobOut]
    total: int
