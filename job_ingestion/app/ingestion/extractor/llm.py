import json
from typing import Literal

from pydantic import BaseModel, Field

from app.llm.base import LLMProvider, LLMResult


class JobEnrichment(BaseModel):
    seniority: Literal["senior", "mid", "junior", "new_grad", "internship", "unclear"]
    is_internship: bool
    is_new_grad: bool
    sponsorship_status: Literal["yes", "no", "unclear"]
    sponsorship_confidence: Literal["high", "low"]
    remote_type: Literal["remote", "hybrid", "onsite", "unclear"]
    tech_stack: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)


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
)


async def enrich_job_text(provider: LLMProvider, clean_text: str) -> LLMResult[JobEnrichment]:
    system_prompt = (
        "You extract structured hiring attributes from job descriptions. "
        "Return only factual values based on provided text."
    )
    user_prompt = f"Job description text:\n{clean_text}"
    return await provider.complete(system_prompt, user_prompt, JobEnrichment)


async def enrich_job_batch_text(
    provider: LLMProvider, jobs: list[dict[str, str]]
) -> LLMResult[BatchJobEnrichmentResponse]:
    system_prompt = (
        "You extract structured hiring attributes from job descriptions. "
        "For each input job, return one output item with the same job_id. "
        "Use factual values from text only."
    )
    user_prompt = (
        "Input jobs JSON array:\n"
        f"{json.dumps(jobs, ensure_ascii=True)}\n\n"
        "Return JSON object with key 'items'."
    )
    return await provider.complete(system_prompt, user_prompt, BatchJobEnrichmentResponse)
