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


class ExtractedContact(BaseModel):
    location: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    email: str | None = None


class ExtractedEducationEntry(BaseModel):
    level: Literal["masters", "undergrad", "doctoral", "other"] = "other"
    degree: str | None = None
    university: str | None = None
    graduation_date: str | None = None
    gpa: str | None = None


class ExtractedEducation(BaseModel):
    degree: str | None = None
    university: str | None = None
    graduation_date: str | None = None
    gpa: str | None = None


class ExtractedSkills(BaseModel):
    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    cloud: list[str] = Field(default_factory=list)
    ai_ml: list[str] = Field(default_factory=list)
    infrastructure: list[str] = Field(default_factory=list)
    product: list[str] = Field(default_factory=list)


SectionOrder = Literal["education_first", "experience_first"]


class LLMExtractionOutput(BaseModel):
    experiences: list[ExtractedExperience] = Field(default_factory=list)
    projects: list[ExtractedProject] = Field(default_factory=list)
    certifications: list[ExtractedCertification] = Field(default_factory=list)
    education: ExtractedEducation = Field(default_factory=ExtractedEducation)
    education_entries: list[ExtractedEducationEntry] = Field(default_factory=list)
    contact: ExtractedContact = Field(default_factory=ExtractedContact)
    skills: ExtractedSkills = Field(default_factory=ExtractedSkills)
    section_order: SectionOrder = "education_first"


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
- Do NOT infer job search preferences, target roles, visa status, sponsorship needs, or location preferences.
- Experience titles are historical job titles from the resume, not target roles the candidate wants to pursue.
- duration_months rules:
  - Compute independently for EACH role from that role's own stated start and end dates.
  - Roles frequently overlap (e.g. part-time research assistant while doing a summer internship).
    Overlapping employment is normal — do NOT subtract one role's months from another.
  - A 3-month summer internship does NOT shorten a concurrent 18-month research role.
  - Extract each overlapping role as a separate experience entry with its full date-range duration.
  - Use inclusive month counting (e.g. Jul 2024 through Dec 2025 ≈ 18 months; May 2025 through Aug 2025 = 4 months).
  - If only a year is given, estimate conservatively for that role alone.
  - Prefer the resume's explicit date range over inferring duration from overlapping roles.
  - Example: "Research Assistant, NYU, Jul 2024 – Dec 2025" and "Intern, Cambium Assessment, May 2025 – Aug 2025"
    → two entries with duration_months 18 and 4 respectively (not 14 or 4 for the RA).
- education_entries: extract each degree separately (undergrad, masters, doctoral) with school, degree, graduation_date, and GPA when present.
- contact: extract location, phone, linkedin, github, and email when explicitly present in the resume header or contact section.
- education (legacy single object): populate with the most recent or highest degree when education_entries is empty.
- section_order: set to education_first when the Education section appears before Experience/Work Experience in the resume; set to experience_first when Experience appears first. Default to education_first for students and early-career resumes when unclear.
- skills: exhaustively parse dedicated Technical Skills / Skills / Core Competencies sections.
  Include every skill listed there (comma-separated lists, bullet lists, and category subsections).
  Map each skill to the best matching category (languages, frameworks, databases, cloud, ai_ml, infrastructure, product).
  Do not omit skills that appear only in a skills section and not in job bullets.

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
