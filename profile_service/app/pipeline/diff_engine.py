from __future__ import annotations

import uuid
from typing import Any

from app.models.evidence import CandidateEvidence
from app.models.profile import CandidateProfile
from app.pipeline.llm_parser import (
    ExtractedContact,
    ExtractedEducation,
    ExtractedEducationEntry,
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


def _education_entry_has_content(entry: ExtractedEducationEntry) -> bool:
    return bool(entry.degree or entry.university or entry.graduation_date)


def _contact_has_content(contact: ExtractedContact) -> bool:
    return bool(contact.location or contact.phone or contact.linkedin or contact.github or contact.email)


def _existing_education_levels(education: dict[str, Any]) -> set[str]:
    levels: set[str] = set()
    for entry in education.get("entries", []) or []:
        level = entry.get("level")
        if level:
            levels.add(str(level))
    if education.get("degree") or education.get("university"):
        degree = str(education.get("degree") or "")
        if degree.lower().startswith(("ms", "m.s", "master", "mba")):
            levels.add("masters")
        elif degree.lower().startswith(("bs", "b.s", "b.tech", "bachelor", "ba", "b.a")):
            levels.add("undergrad")
        else:
            levels.add("other")
    return levels


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

    current_education = (current_profile.education if current_profile else {}) or {}

    if _contact_has_content(extracted.contact):
        current_contact = current_education.get("contact") or {}
        if not any(current_contact.get(k) for k in ("location", "phone", "linkedin", "github")):
            operations.append(
                {
                    "op": "ADD_CONTACT",
                    "data": extracted.contact.model_dump(exclude={"email"}),
                }
            )
        else:
            for field in ("location", "phone", "linkedin", "github"):
                new_value = getattr(extracted.contact, field)
                old_value = current_contact.get(field)
                if new_value and new_value != old_value:
                    operations.append(
                        {
                            "op": "UPDATE_CONTACT",
                            "field": field,
                            "from": old_value,
                            "to": new_value,
                        }
                    )

    education_entries = extracted.education_entries or []
    if not education_entries and _education_has_content(extracted.education):
        degree = extracted.education.degree or ""
        level = "other"
        lowered = degree.lower()
        if lowered.startswith(("ms", "m.s", "master", "mba")):
            level = "masters"
        elif lowered.startswith(("bs", "b.s", "b.tech", "bachelor", "ba", "b.a")):
            level = "undergrad"
        elif lowered.startswith(("phd", "doctor")):
            level = "doctoral"
        education_entries = [
            ExtractedEducationEntry(
                level=level,
                degree=extracted.education.degree,
                university=extracted.education.university,
                graduation_date=extracted.education.graduation_date,
                gpa=extracted.education.gpa,
            )
        ]

    operations.append(
        {
            "op": "SET_SECTION_ORDER",
            "value": extracted.section_order,
        }
    )

    existing_levels = _existing_education_levels(current_education)
    for entry in education_entries:
        if not _education_entry_has_content(entry):
            continue
        if entry.level not in existing_levels:
            operations.append(
                {
                    "op": "ADD_EDUCATION_ENTRY",
                    "data": entry.model_dump(),
                }
            )
            existing_levels.add(entry.level)

    return _assign_op_ids(operations)
