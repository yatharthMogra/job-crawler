from __future__ import annotations

import uuid
from typing import Any

from app.models.evidence import CandidateEvidence
from app.models.profile import CandidateProfile
from app.pipeline.llm_parser import (
    ExtractedEducation,
    ExtractedExperience,
    ExtractedProject,
    LLMExtractionOutput,
)
from app.utils.text_utils import (
    find_experience_merge_candidate,
    find_project_merge_candidate,
    normalize_skill,
)


def _assign_op_ids(operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for op in operations:
        op.setdefault("id", str(uuid.uuid4()))
    return operations


def _compute_experience_diffs(
    extracted: ExtractedExperience,
    existing: CandidateEvidence,
) -> list[dict[str, Any]]:
    diffs: list[dict[str, Any]] = []
    data = existing.normalized_data
    fields = {
        "title": extracted.title,
        "company": extracted.company,
        "duration_months": extracted.duration_months,
        "domains": extracted.domains,
        "evidence_keywords": extracted.evidence_keywords,
    }
    for field, new_value in fields.items():
        old_value = data.get(field)
        if old_value != new_value:
            diffs.append(
                {
                    "op": "UPDATE_EXPERIENCE",
                    "evidence_id": str(existing.id),
                    "field": field,
                    "from": old_value,
                    "to": new_value,
                }
            )
    return diffs


def _education_has_content(education: ExtractedEducation) -> bool:
    return bool(education.degree or education.university or education.graduation_date)


def compute_proposed_operations(
    extracted: LLMExtractionOutput,
    current_profile: CandidateProfile | None,
    current_evidence: list[CandidateEvidence],
) -> list[dict[str, Any]]:
    operations: list[dict[str, Any]] = []

    existing_skills = (current_profile.skills if current_profile else {}) or {}
    for category in (
        "languages",
        "frameworks",
        "databases",
        "cloud",
        "ai_ml",
        "infrastructure",
        "product",
    ):
        new_skills = getattr(extracted.skills, category, [])
        category_skills = existing_skills.get(category, [])
        for skill in new_skills:
            normalized = normalize_skill(skill)
            if normalized not in category_skills:
                operations.append(
                    {
                        "op": "ADD_SKILL",
                        "category": category,
                        "value": normalized,
                    }
                )

    for exp in extracted.experiences:
        merge_candidate = find_experience_merge_candidate(exp, current_evidence)
        if merge_candidate is None:
            operations.append(
                {
                    "op": "ADD_EXPERIENCE",
                    "data": exp.model_dump(),
                }
            )
        else:
            operations.extend(_compute_experience_diffs(exp, merge_candidate))

    for project in extracted.projects:
        merge_candidate = find_project_merge_candidate(project.name, current_evidence)
        if merge_candidate is None:
            operations.append(
                {
                    "op": "ADD_PROJECT",
                    "data": project.model_dump(),
                }
            )
        else:
            data = merge_candidate.normalized_data
            for field in ("category", "domains", "evidence_keywords"):
                new_value = getattr(project, field)
                old_value = data.get(field)
                if old_value != new_value:
                    operations.append(
                        {
                            "op": "UPDATE_PROJECT",
                            "evidence_id": str(merge_candidate.id),
                            "field": field,
                            "from": old_value,
                            "to": new_value,
                        }
                    )

    for cert in extracted.certifications:
        operations.append(
            {
                "op": "ADD_CERTIFICATION",
                "data": cert.model_dump(),
            }
        )

    if _education_has_content(extracted.education):
        current_education = (current_profile.education if current_profile else {}) or {}
        if not any(current_education.get(k) for k in ("degree", "university", "graduation_date")):
            operations.append(
                {
                    "op": "ADD_EDUCATION",
                    "data": extracted.education.model_dump(),
                }
            )
        else:
            for field in ("degree", "university", "graduation_date"):
                new_value = getattr(extracted.education, field)
                old_value = current_education.get(field)
                if new_value and new_value != old_value:
                    operations.append(
                        {
                            "op": "UPDATE_EDUCATION",
                            "field": field,
                            "from": old_value,
                            "to": new_value,
                        }
                    )

    suggestions = extracted.constraint_suggestions.model_dump(exclude_none=True)
    for field, suggested_value in suggestions.items():
        operations.append(
            {
                "op": "ADD_CONSTRAINT_SUGGESTION",
                "field": field,
                "suggested_value": suggested_value,
            }
        )

    pref_suggestions = extracted.preference_suggestions.model_dump(exclude_none=True)
    for field, suggested_value in pref_suggestions.items():
        if isinstance(suggested_value, list) and not suggested_value:
            continue
        if suggested_value is None:
            continue
        operations.append(
            {
                "op": "ADD_PREFERENCE_SUGGESTION",
                "field": field,
                "suggested_value": suggested_value,
            }
        )

    return _assign_op_ids(operations)
