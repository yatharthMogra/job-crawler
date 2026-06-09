from __future__ import annotations

import re
from typing import TYPE_CHECKING

from rapidfuzz import fuzz

if TYPE_CHECKING:
    from app.models.evidence import CandidateEvidence
    from app.pipeline.llm_parser import ExtractedExperience


SKILL_ALIAS_MAP: dict[str, str] = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "nodejs": "Node.js",
    "node": "Node.js",
    "node.js": "Node.js",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "aws": "AWS",
    "py": "Python",
    "python3": "Python",
}


def normalize_skill(skill: str) -> str:
    key = skill.lower().strip()
    return SKILL_ALIAS_MAP.get(key, skill.strip())


def normalize_company(name: str) -> str:
    cleaned = re.sub(r"[^\w\s]", "", name.lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    suffixes = (" inc", " llc", " ltd", " corp", " corporation", " co")
    for suffix in suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)].strip()
    return cleaned


def title_similarity(a: str, b: str) -> float:
    return fuzz.token_sort_ratio(a.lower(), b.lower()) / 100.0


def find_experience_merge_candidate(
    extracted_exp: ExtractedExperience,
    existing_evidence: list[CandidateEvidence],
) -> CandidateEvidence | None:
    best: CandidateEvidence | None = None
    best_score = 0.0
    extracted_company = normalize_company(extracted_exp.company)

    for item in existing_evidence:
        if item.evidence_type != "experience" or not item.is_active:
            continue
        data = item.normalized_data
        company = normalize_company(str(data.get("company", "")))
        if company != extracted_company:
            continue
        title = str(data.get("title", ""))
        score = title_similarity(extracted_exp.title, title)
        if score > 0.8 and score > best_score:
            best = item
            best_score = score
    return best


def find_project_merge_candidate(
    project_name: str,
    existing_evidence: list[CandidateEvidence],
) -> CandidateEvidence | None:
    normalized = project_name.lower().strip()
    for item in existing_evidence:
        if item.evidence_type != "project" or not item.is_active:
            continue
        existing_name = str(item.normalized_data.get("name", "")).lower().strip()
        if existing_name == normalized:
            return item
        if fuzz.token_sort_ratio(normalized, existing_name) > 85:
            return item
    return None


def is_garbage_text(text: str) -> bool:
    if not text.strip():
        return True
    printable = sum(1 for c in text if c.isprintable() or c.isspace())
    ratio = printable / max(len(text), 1)
    return ratio < 0.7


def default_constraints() -> dict:
    return {
        "sponsorship_required": False,
        "visa_type": None,
        "work_authorization": None,
        "internship_only": False,
        "fulltime_only": False,
        "minimum_salary": None,
        "minimum_hourly_rate": None,
        "target_seniority": ["INTERN", "NEW_GRAD", "ENTRY", "MID", "JUNIOR"],
        "eeo": {},
    }


def default_preferences() -> dict:
    return {
        "primary_roles": [],
        "secondary_roles": [],
        "preferred_locations": [],
        "acceptable_locations": [],
        "remote_preference": None,
        "relocation_allowed": False,
        "preferred_company_stages": [],
        "preferred_industries": [],
    }


def default_skills() -> dict:
    return {
        "languages": [],
        "frameworks": [],
        "databases": [],
        "cloud": [],
        "ai_ml": [],
        "infrastructure": [],
        "product": [],
    }


def default_education() -> dict:
    return {
        "section_order": "education_first",
        "contact": {
            "location": None,
            "phone": None,
            "linkedin": None,
            "github": None,
        },
        "entries": [],
        "degree": None,
        "university": None,
        "graduation_date": None,
        "gpa": None,
    }
