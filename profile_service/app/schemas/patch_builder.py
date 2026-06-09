from __future__ import annotations

import uuid
from typing import Any

from app.schemas.patch import PatchOperationResponse, PendingPatchResponse
from app.models.patch import CandidatePatch


def _to_operation(op: dict[str, Any]) -> PatchOperationResponse:
    payload = dict(op)
    if "from" in payload:
        payload["from_value"] = payload.pop("from")
    return PatchOperationResponse.model_validate(payload)


def build_pending_patch_response(patch: CandidatePatch) -> PendingPatchResponse:
    skills: list[PatchOperationResponse] = []
    experiences: list[PatchOperationResponse] = []
    projects: list[PatchOperationResponse] = []
    certifications: list[PatchOperationResponse] = []
    education: list[PatchOperationResponse] = []
    constraints: list[PatchOperationResponse] = []
    preferences: list[PatchOperationResponse] = []

    for op in patch.proposed_operations:
        operation = _to_operation(op)
        match op.get("op"):
            case "ADD_SKILL":
                skills.append(operation)
            case "ADD_EXPERIENCE" | "UPDATE_EXPERIENCE":
                experiences.append(operation)
            case "ADD_PROJECT" | "UPDATE_PROJECT":
                projects.append(operation)
            case "ADD_CERTIFICATION":
                certifications.append(operation)
            case (
                "ADD_EDUCATION"
                | "UPDATE_EDUCATION"
                | "ADD_EDUCATION_ENTRY"
                | "ADD_CONTACT"
                | "UPDATE_CONTACT"
                | "SET_SECTION_ORDER"
            ):
                education.append(operation)
            case "ADD_CONSTRAINT_SUGGESTION":
                constraints.append(operation)
            case "ADD_PREFERENCE_SUGGESTION":
                preferences.append(operation)

    return PendingPatchResponse(
        patch_id=patch.id,
        candidate_id=patch.candidate_id,
        source_resume_id=patch.source_resume_id,
        profile_version_before=patch.profile_version_before,
        status=patch.status,
        created_at=patch.created_at,
        skills=skills,
        experiences=experiences,
        projects=projects,
        certifications=certifications,
        education=education,
        constraints=constraints,
        preferences=preferences,
    )
