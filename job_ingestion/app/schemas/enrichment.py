from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JobEnrichmentOut(BaseModel):
    id: str
    status: str
    failure_reason: Optional[str]
    llm_provider: Optional[str]
    llm_model: Optional[str]
    extraction_version: Optional[str]
    seniority: Optional[str]
    is_internship: Optional[bool]
    is_new_grad: Optional[bool]
    sponsorship_status: Optional[str]
    sponsorship_confidence: Optional[str]
    remote_type: Optional[str]
    tech_stack: list[str]
    skills: list[str]
    normalized_roles: list[str] = []
    job_capabilities: list[str] = []
    application_effort: Optional[str] = None
    retrieval_pools: list[str] = []
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    opportunity_score: Optional[float] = None
    opportunity_score_computed_at: Optional[datetime] = None
    responsibilities: list[str] = []
    required_qualifications: list[str] = []
    preferred_qualifications: list[str] = []
    benefits: list[str] = []
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    latency_ms: Optional[int]
    created_at: datetime
