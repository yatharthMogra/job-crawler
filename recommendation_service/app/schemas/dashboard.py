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


class DashboardJobsResponse(BaseModel):
    jobs: list[DashboardJobOut]
    total: int
