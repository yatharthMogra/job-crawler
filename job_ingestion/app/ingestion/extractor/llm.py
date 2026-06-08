from __future__ import annotations

import json
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.ingestion.constants_taxonomy import CAPABILITY_TAXONOMY, NORMALIZED_ROLES
from app.llm.base import LLMProvider, LLMResult

NormalizedRole = Literal[
    "SWE",
    "BACKEND_ENGINEER",
    "FRONTEND_ENGINEER",
    "FULLSTACK_ENGINEER",
    "ML_ENGINEER",
    "DATA_ENGINEER",
    "DATA_SCIENTIST",
    "DEVOPS_ENGINEER",
    "SECURITY_ENGINEER",
    "MOBILE_ENGINEER",
    "PRODUCT_MANAGER",
    "OTHER",
]

CapabilityName = Literal[
    "Backend Engineering",
    "Frontend Engineering",
    "Full Stack Development",
    "AI Systems",
    "Machine Learning",
    "Machine Learning Research",
    "Data Engineering",
    "Distributed Systems",
    "Cloud Infrastructure",
    "Platform Engineering",
    "DevOps",
    "Product Engineering",
    "Mobile Development",
    "Security Engineering",
    "Analytics Engineering",
    "Research",
]

ApplicationEffort = Literal["LOW", "MEDIUM", "HIGH"]

ENRICHMENT_SYSTEM_PROMPT = (
    "You extract structured hiring attributes from job descriptions. "
    "For each input job, return one output item with the same job_id. "
    "Use factual values from text only.\n\n"
    "normalized_roles rules:\n"
    "- Assign ALL applicable roles from the taxonomy, not just the primary one\n"
    "- A 'ML Infrastructure Engineer' gets both ML_ENGINEER and BACKEND_ENGINEER\n"
    "- When uncertain, assign OTHER rather than forcing an incorrect role\n"
    "- Never assign roles not in the taxonomy\n"
    f"- Taxonomy: {', '.join(NORMALIZED_ROLES)}\n\n"
    "job_capabilities rules:\n"
    "- Assign capabilities the job requires from the taxonomy only\n"
    f"- Taxonomy: {', '.join(CAPABILITY_TAXONOMY)}\n\n"
    "application_effort rules:\n"
    "- REQUIRED field: LOW, MEDIUM, or HIGH — never null; use MEDIUM when unclear\n"
    "- LOW: one-click apply, resume upload only, no cover letter required\n"
    "- MEDIUM: resume + standard questions, short cover letter optional\n"
    "- HIGH: cover letter required, portfolio required, screening questions, "
    "multi-step application form\n\n"
    "salary_min and salary_max:\n"
    "- Extract annual USD salary range when explicitly stated\n"
    "- Leave null when not mentioned or only hourly/equity is given\n\n"
    "tech_stack rules:\n"
    "- REQUIRED for engineering roles (SWE, BACKEND_ENGINEER, FRONTEND_ENGINEER, "
    "FULLSTACK_ENGINEER, ML_ENGINEER, DATA_ENGINEER, DATA_SCIENTIST, DEVOPS_ENGINEER, "
    "SECURITY_ENGINEER, MOBILE_ENGINEER): return at least 3 items; never []\n"
    "- List explicit tools, languages, frameworks, databases, and cloud platforms\n"
    "- Use canonical names (Python, Go, Java, TypeScript, React, Kubernetes, AWS, "
    "GCP, PostgreSQL, Spark, PyTorch, etc.)\n"
    "- Leave empty only for non-technical roles (e.g. PRODUCT_MANAGER, sales, legal)\n\n"
    "skills rules:\n"
    "- REQUIRED alongside tech_stack for engineering roles: return at least 2 domain "
    "competencies or technical themes\n"
    "- Examples: distributed systems, NLP, computer vision, CI/CD, data pipelines\n"
    "- Do not duplicate job_capabilities taxonomy labels here\n"
    "- Leave empty only when no technical themes are present"
)


_ENGINEERING_ROLES = frozenset(
    {
        "SWE",
        "BACKEND_ENGINEER",
        "FRONTEND_ENGINEER",
        "FULLSTACK_ENGINEER",
        "ML_ENGINEER",
        "DATA_ENGINEER",
        "DATA_SCIENTIST",
        "DEVOPS_ENGINEER",
        "SECURITY_ENGINEER",
        "MOBILE_ENGINEER",
    }
)


def enrichment_missing_skill_fields(
    tech_stack: list[str],
    skills: list[str],
    *,
    description_chars: int,
    normalized_roles: list[str] | None = None,
    min_description_chars: int = 300,
) -> bool:
    """True when a substantive engineering job yielded no skill signals."""
    if tech_stack or skills:
        return False
    if description_chars < min_description_chars:
        return False
    if normalized_roles and not (set(normalized_roles) & _ENGINEERING_ROLES):
        return False
    return True


class JobEnrichment(BaseModel):
    seniority: Literal["senior", "mid", "junior", "new_grad", "internship", "unclear"]
    is_internship: bool
    is_new_grad: bool
    sponsorship_status: Literal["yes", "no", "unclear"]
    sponsorship_confidence: Literal["high", "low"]
    remote_type: Literal["remote", "hybrid", "onsite", "unclear"]
    tech_stack: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    normalized_roles: list[NormalizedRole] = Field(default_factory=lambda: ["OTHER"])
    job_capabilities: list[CapabilityName] = Field(default_factory=list)
    application_effort: ApplicationEffort = "MEDIUM"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None

    @field_validator("application_effort", mode="before")
    @classmethod
    def _default_application_effort(cls, value: object) -> object:
        return "MEDIUM" if value is None else value


class BatchJobEnrichment(BaseModel):
    job_id: str
    seniority: Literal["senior", "mid", "junior", "new_grad", "internship", "unclear"] = "unclear"
    is_internship: bool = False
    is_new_grad: bool = False
    sponsorship_status: Literal["yes", "no", "unclear"] = "unclear"
    sponsorship_confidence: Literal["high", "low"] = "low"
    remote_type: Literal["remote", "hybrid", "onsite", "unclear"] = "unclear"
    tech_stack: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    normalized_roles: list[NormalizedRole] = Field(default_factory=lambda: ["OTHER"])
    job_capabilities: list[CapabilityName] = Field(default_factory=list)
    application_effort: ApplicationEffort = "MEDIUM"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None

    @field_validator("application_effort", mode="before")
    @classmethod
    def _default_application_effort(cls, value: object) -> object:
        return "MEDIUM" if value is None else value


class BatchJobEnrichmentResponse(BaseModel):
    items: list[BatchJobEnrichment] = Field(default_factory=list)


DEFAULT_ENRICHMENT = JobEnrichment(
    seniority="unclear",
    is_internship=False,
    is_new_grad=False,
    sponsorship_status="unclear",
    sponsorship_confidence="low",
    remote_type="unclear",
    tech_stack=[],
    skills=[],
    normalized_roles=["OTHER"],
    job_capabilities=[],
    application_effort="MEDIUM",
    salary_min=None,
    salary_max=None,
)


async def enrich_job_text(provider: LLMProvider, clean_text: str) -> LLMResult[JobEnrichment]:
    user_prompt = f"Job description text:\n{clean_text}"
    return await provider.complete(ENRICHMENT_SYSTEM_PROMPT, user_prompt, JobEnrichment)


async def enrich_job_batch_text(
    provider: LLMProvider, jobs: list[dict[str, str]]
) -> LLMResult[BatchJobEnrichmentResponse]:
    user_prompt = (
        "Input jobs JSON array:\n"
        f"{json.dumps(jobs, ensure_ascii=True)}\n\n"
        "Return JSON object with key 'items'."
    )
    return await provider.complete(ENRICHMENT_SYSTEM_PROMPT, user_prompt, BatchJobEnrichmentResponse)
