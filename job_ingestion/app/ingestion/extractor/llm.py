from __future__ import annotations

import json
import re
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator

from app.ingestion.constants_taxonomy import (
    CAPABILITY_TAXONOMY,
    ENGINEERING_ROLES,
    NORMALIZED_ROLES,
    ROLE_CLASSIFICATION_RULES,
)

_VALID_NORMALIZED_ROLES = frozenset(NORMALIZED_ROLES)
_VALID_CAPABILITIES = frozenset(CAPABILITY_TAXONOMY)

from app.ingestion.extractor.seniority import (
    SENIORITY_PROMPT_RULES,
    apply_seniority_consistency,
    normalize_seniority,
)
from app.ingestion.taxonomy import (
    DOMAIN_PROMPT_RULES,
    coerce_job_domain,
    sanitize_job_secondary_domain,
)
from app.llm.base import LLMProvider, LLMResult

def _coerce_normalized_roles(value: object) -> list[str]:
    if not isinstance(value, list):
        return ["OTHER"]
    roles: list[str] = []
    for item in value:
        role = str(item).strip().upper().replace(" ", "_").replace("-", "_")
        if role in _VALID_NORMALIZED_ROLES:
            roles.append(role)
    return roles or ["OTHER"]


def _coerce_salary(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, float):
        if value != value or value <= 0:
            return None
        return int(round(value))
    if isinstance(value, str):
        stripped = value.strip().replace(",", "").replace("$", "")
        if not stripped:
            return None
        multiplier = 1
        lowered = stripped.lower()
        if lowered.endswith("k"):
            stripped = stripped[:-1]
            multiplier = 1000
        elif lowered.endswith("m"):
            stripped = stripped[:-1]
            multiplier = 1_000_000
        try:
            amount = float(stripped) * multiplier
            return int(round(amount)) if amount > 0 else None
        except ValueError:
            return None
    return None


def _coerce_job_capabilities(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    capabilities: list[str] = []
    for item in value:
        name = str(item).strip()
        if name in _VALID_CAPABILITIES:
            capabilities.append(name)
    return capabilities


def _strip_json_fences(text: str) -> str:
    value = text.strip()
    if not value:
        return value
    fenced_match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", value, flags=re.IGNORECASE | re.DOTALL)
    if fenced_match:
        return fenced_match.group(1).strip()
    inline_match = re.search(r"```(?:json)?\s*(.*?)\s*```", value, flags=re.IGNORECASE | re.DOTALL)
    if inline_match:
        return inline_match.group(1).strip()
    return value


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
SeniorityLevel = Literal[
    "INTERN",
    "NEW_GRAD",
    "ENTRY",
    "JUNIOR",
    "MID",
    "SENIOR",
    "STAFF",
    "PRINCIPAL",
    "MANAGEMENT",
    "UNKNOWN",
]

ENRICHMENT_SYSTEM_PROMPT = (
    "You extract structured hiring attributes from job descriptions. "
    "For each input job, return one output item with the same job_id. "
    "Use factual values from text only.\n\n"
    f"{SENIORITY_PROMPT_RULES}\n"
    "normalized_roles rules:\n"
    "- Assign ALL applicable roles from the taxonomy, not just the primary one\n"
    "- A 'ML Infrastructure Engineer' gets both ML_ENGINEER and BACKEND_ENGINEER\n"
    "- Never assign roles not in the taxonomy\n"
    f"- Taxonomy: {', '.join(NORMALIZED_ROLES)}\n"
    f"{ROLE_CLASSIFICATION_RULES}\n\n"
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
    "SECURITY_ENGINEER, MOBILE_ENGINEER, SOLUTIONS_ENGINEER, SUPPORT_ENGINEER, "
    "SYSTEMS_ENGINEER, HARDWARE_ENGINEER): "
    "return at least 3 items; never []\n"
    "- List explicit tools, languages, frameworks, databases, and cloud platforms\n"
    "- Use canonical names (Python, Go, Java, TypeScript, React, Kubernetes, AWS, "
    "GCP, PostgreSQL, Spark, PyTorch, etc.)\n"
    "- Leave empty only for non-technical roles (e.g. SALES, FINANCE, LEGAL, RECRUITING)\n\n"
    "skills rules:\n"
    "- REQUIRED alongside tech_stack for engineering roles: return at least 2 domain "
    "competencies or technical themes\n"
    "- Examples: distributed systems, NLP, computer vision, CI/CD, data pipelines\n"
    "- Do not duplicate job_capabilities taxonomy labels here\n"
    "- Leave empty only when no technical themes are present\n\n"
    f"{DOMAIN_PROMPT_RULES}"
)


class _DomainFieldsMixin(BaseModel):
    job_domain: str = "Other"
    job_secondary_domain: Optional[str] = None

    @field_validator("job_domain", mode="before")
    @classmethod
    def _coerce_job_domain(cls, value: object) -> str:
        return coerce_job_domain(value)

    @model_validator(mode="after")
    def _sanitize_secondary_domain(self) -> _DomainFieldsMixin:
        self.job_secondary_domain = sanitize_job_secondary_domain(
            self.job_domain,
            self.job_secondary_domain,
        )
        return self


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
    if normalized_roles and not (set(normalized_roles) & ENGINEERING_ROLES):
        return False
    return True


class JobEnrichment(_DomainFieldsMixin):
    seniority: SeniorityLevel = "UNKNOWN"
    is_internship: bool
    is_new_grad: bool
    sponsorship_status: Literal["yes", "no", "unclear"]
    sponsorship_confidence: Literal["high", "low"]
    remote_type: Literal["remote", "hybrid", "onsite", "unclear"]
    tech_stack: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    normalized_roles: list[str] = Field(default_factory=lambda: ["OTHER"])
    job_capabilities: list[CapabilityName] = Field(default_factory=list)
    application_effort: ApplicationEffort = "MEDIUM"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None

    @field_validator("normalized_roles", mode="before")
    @classmethod
    def _validate_normalized_roles(cls, value: object) -> list[str]:
        return _coerce_normalized_roles(value)

    @field_validator("seniority", mode="before")
    @classmethod
    def _normalize_seniority(cls, value: object) -> str:
        return normalize_seniority(str(value) if value is not None else None)

    @field_validator("application_effort", mode="before")
    @classmethod
    def _default_application_effort(cls, value: object) -> object:
        return "MEDIUM" if value is None else value

    @field_validator("salary_min", "salary_max", mode="before")
    @classmethod
    def _coerce_salary_fields(cls, value: object) -> int | None:
        return _coerce_salary(value)

    @field_validator("job_capabilities", mode="before")
    @classmethod
    def _coerce_capabilities(cls, value: object) -> list[str]:
        return _coerce_job_capabilities(value)


class BatchJobEnrichment(_DomainFieldsMixin):
    job_id: str
    seniority: SeniorityLevel = "UNKNOWN"
    is_internship: bool = False
    is_new_grad: bool = False
    sponsorship_status: Literal["yes", "no", "unclear"] = "unclear"
    sponsorship_confidence: Literal["high", "low"] = "low"
    remote_type: Literal["remote", "hybrid", "onsite", "unclear"] = "unclear"
    tech_stack: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    normalized_roles: list[str] = Field(default_factory=lambda: ["OTHER"])
    job_capabilities: list[CapabilityName] = Field(default_factory=list)
    application_effort: ApplicationEffort = "MEDIUM"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None

    @field_validator("normalized_roles", mode="before")
    @classmethod
    def _validate_normalized_roles(cls, value: object) -> list[str]:
        return _coerce_normalized_roles(value)

    @field_validator("seniority", mode="before")
    @classmethod
    def _normalize_seniority(cls, value: object) -> str:
        return normalize_seniority(str(value) if value is not None else None)

    @field_validator("application_effort", mode="before")
    @classmethod
    def _default_application_effort(cls, value: object) -> object:
        return "MEDIUM" if value is None else value

    @field_validator("salary_min", "salary_max", mode="before")
    @classmethod
    def _coerce_salary_fields(cls, value: object) -> int | None:
        return _coerce_salary(value)

    @field_validator("job_capabilities", mode="before")
    @classmethod
    def _coerce_capabilities(cls, value: object) -> list[str]:
        return _coerce_job_capabilities(value)


class BatchJobEnrichmentResponse(BaseModel):
    items: list[BatchJobEnrichment] = Field(default_factory=list)


def parse_batch_enrichment_response(text: str) -> BatchJobEnrichmentResponse:
    """Parse batch LLM output, validating each item independently."""
    candidates = [text.strip()]
    sanitized = _strip_json_fences(text)
    if sanitized and sanitized != candidates[0]:
        candidates.append(sanitized)

    last_error: Exception | None = None
    for candidate in candidates:
        if not candidate:
            continue
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = exc
            continue
        if not isinstance(data, dict):
            continue
        items_raw = data.get("items")
        if not isinstance(items_raw, list):
            continue
        validated: list[BatchJobEnrichment] = []
        for entry in items_raw:
            if not isinstance(entry, dict):
                continue
            try:
                validated.append(BatchJobEnrichment.model_validate(entry))
            except Exception as exc:
                last_error = exc
                continue
        if validated:
            return BatchJobEnrichmentResponse(items=validated)

    if last_error is not None:
        raise ValueError(f"Failed to parse batch enrichment response: {last_error}") from last_error
    raise ValueError("Failed to parse batch enrichment response: empty or invalid JSON")


DEFAULT_ENRICHMENT = JobEnrichment(
    seniority="UNKNOWN",
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


EnrichmentLike = Union[JobEnrichment, BatchJobEnrichment]


def finalize_enrichment(
    enrichment: EnrichmentLike,
    *,
    title: str | None = None,
    employment_type: str | None = None,
) -> EnrichmentLike:
    seniority, is_internship, is_new_grad = apply_seniority_consistency(
        enrichment.seniority,
        enrichment.is_internship,
        enrichment.is_new_grad,
        title=title,
        employment_type=employment_type,
    )
    updates = {
        "seniority": seniority,
        "is_internship": is_internship,
        "is_new_grad": is_new_grad,
    }
    return enrichment.model_copy(update=updates)


async def enrich_job_text(
    provider: LLMProvider,
    clean_text: str,
    *,
    title: str | None = None,
    employment_type: str | None = None,
) -> LLMResult[JobEnrichment]:
    context_parts: list[str] = []
    if title:
        context_parts.append(f"Job title: {title}")
    if employment_type:
        context_parts.append(f"Employment type: {employment_type}")
    context = "\n".join(context_parts)
    user_prompt = f"{context}\n\nJob description text:\n{clean_text}" if context else f"Job description text:\n{clean_text}"
    result = await provider.complete(ENRICHMENT_SYSTEM_PROMPT, user_prompt, JobEnrichment)
    finalized = finalize_enrichment(result.output, title=title, employment_type=employment_type)
    return LLMResult(
        output=finalized,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        latency_ms=result.latency_ms,
    )


async def enrich_job_batch_text(
    provider: LLMProvider, jobs: list[dict[str, str]]
) -> LLMResult[BatchJobEnrichmentResponse]:
    user_prompt = (
        "Input jobs JSON array:\n"
        f"{json.dumps(jobs, ensure_ascii=True)}\n\n"
        "Return JSON object with key 'items'."
    )
    text_result = await provider.generate_text(ENRICHMENT_SYSTEM_PROMPT, user_prompt)
    parsed = parse_batch_enrichment_response(text_result.output)
    jobs_by_id = {job["job_id"]: job for job in jobs}
    finalized_items: list[BatchJobEnrichment] = []
    for item in parsed.items:
        source = jobs_by_id.get(item.job_id, {})
        finalized_items.append(
            finalize_enrichment(
                item,
                title=source.get("title"),
                employment_type=source.get("employment_type"),
            )
        )
    finalized_response = BatchJobEnrichmentResponse(items=finalized_items)
    return LLMResult(
        output=finalized_response,
        input_tokens=text_result.input_tokens,
        output_tokens=text_result.output_tokens,
        latency_ms=text_result.latency_ms,
    )
