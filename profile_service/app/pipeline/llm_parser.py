from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

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


class ExtractedExperience(BaseModel):
    title: str
    company: str
    duration_months: int
    domains: list[str] = Field(default_factory=list)
    evidence_keywords: list[str] = Field(default_factory=list)


class ExtractedProject(BaseModel):
    name: str
    category: str
    domains: list[str] = Field(default_factory=list)
    evidence_keywords: list[str] = Field(default_factory=list)


class ExtractedCertification(BaseModel):
    name: str
    issuer: str


class ExtractedEducation(BaseModel):
    degree: str | None = None
    university: str | None = None
    graduation_date: str | None = None


class ExtractedSkills(BaseModel):
    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    cloud: list[str] = Field(default_factory=list)
    ai_ml: list[str] = Field(default_factory=list)
    infrastructure: list[str] = Field(default_factory=list)
    product: list[str] = Field(default_factory=list)


class ConstraintSuggestions(BaseModel):
    sponsorship_required: bool | None = None
    visa_type: str | None = None
    work_authorization: str | None = None
    internship_only: bool | None = None
    fulltime_only: bool | None = None


class PreferenceSuggestions(BaseModel):
    primary_roles: list[str] = Field(default_factory=list)
    secondary_roles: list[str] = Field(default_factory=list)
    preferred_locations: list[str] = Field(default_factory=list)
    remote_preference: str | None = None
    preferred_industries: list[str] = Field(default_factory=list)


class LLMExtractionOutput(BaseModel):
    experiences: list[ExtractedExperience] = Field(default_factory=list)
    projects: list[ExtractedProject] = Field(default_factory=list)
    certifications: list[ExtractedCertification] = Field(default_factory=list)
    education: ExtractedEducation = Field(default_factory=ExtractedEducation)
    skills: ExtractedSkills = Field(default_factory=ExtractedSkills)
    constraint_suggestions: ConstraintSuggestions = Field(default_factory=ConstraintSuggestions)
    preference_suggestions: PreferenceSuggestions = Field(default_factory=PreferenceSuggestions)


class InferredCapability(BaseModel):
    name: CapabilityName
    supporting_evidence: list[str] = Field(default_factory=list)


class CapabilityInferenceOutput(BaseModel):
    capabilities: list[InferredCapability] = Field(default_factory=list)


EXTRACTION_SYSTEM_PROMPT = """You are a precise resume parser. Extract structured professional information from the resume text provided.

Rules:
- Extract ONLY information explicitly present in the resume text.
- Do not infer, embellish, or hallucinate details.
- evidence_keywords must be normalized technical/architectural signals, not raw bullet text.
- For constraint and preference suggestions: only suggest when there are clear signals. Leave null if uncertain.
- duration_months: compute from date ranges if present. If only year given, estimate conservatively.
- education: extract degree, university, and graduation_date when present.

Return a single JSON object matching the provided schema exactly."""

CAPABILITY_SYSTEM_PROMPT = """Given the following extracted evidence and skills from a candidate's resume, assign capabilities from the provided taxonomy only.

Rules:
- Only assign a capability if there is direct evidence supporting it.
- supporting_evidence must reference specific companies, project names, or concrete technical signals from the evidence.
- Do not assign capabilities not present in the taxonomy.
- Do not invent new capability names.

Taxonomy (choose only from this list):
Backend Engineering, Frontend Engineering, Full Stack Development, AI Systems, Machine Learning,
Machine Learning Research, Data Engineering, Distributed Systems, Cloud Infrastructure,
Platform Engineering, DevOps, Product Engineering, Mobile Development, Security Engineering,
Analytics Engineering, Research"""


async def extract_resume_evidence(
    raw_text: str,
    llm_provider,
) -> LLMExtractionOutput:
    user_prompt = f"Resume text:\n\n{raw_text}"
    result = await llm_provider.complete(
        EXTRACTION_SYSTEM_PROMPT,
        user_prompt,
        LLMExtractionOutput,
    )
    return result.output


async def infer_capabilities(
    evidence_summary: str,
    llm_provider,
) -> CapabilityInferenceOutput:
    user_prompt = f"Evidence and skills summary:\n\n{evidence_summary}"
    result = await llm_provider.complete(
        CAPABILITY_SYSTEM_PROMPT,
        user_prompt,
        CapabilityInferenceOutput,
    )
    return result.output
