from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DashboardJobOut(BaseModel):
    id: uuid.UUID
    title: str
    company_name: str
    location: Optional[str]
    posting_url: Optional[str]
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


class H1BSponsorshipInfo(BaseModel):
    pool_family: str
    total_lca_3yr: int
    approval_rate_3yr: float | None
    is_top_sponsor: bool
    years_covered: list[int]


class DashboardRecommendedJobOut(DashboardJobOut):
    personal_score: float
    match_reasons: list[str] = Field(default_factory=list)
    h1b_sponsorship: H1BSponsorshipInfo | None = None


class DashboardJobsResponse(BaseModel):
    jobs: list[DashboardJobOut]
    total: int


class DashboardRecommendedJobsResponse(BaseModel):
    jobs: list[DashboardRecommendedJobOut]
    total: int
