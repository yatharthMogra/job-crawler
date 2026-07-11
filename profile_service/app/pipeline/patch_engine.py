from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import delete, select, text as sql_text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.exceptions import ConflictError, NotFoundError
from app.llm.factory import get_llm_provider
from app.models.evidence import CandidateEvidence
from app.models.patch import CandidatePatch
from app.models.profile import CandidateProfile
from app.models.resume import CandidateResume
from app.pipeline.capability_engine import recompute_capabilities
from app.experience_tier_sync import refresh_experience_tier_constraints
from app.pipeline.diff_engine import compute_proposed_operations
from app.pipeline.extractor import extract_text
from app.pipeline.llm_parser import extract_resume_evidence
from app.storage import get_resume_storage
from app.utils.constraints import normalize_constraints
from app.utils.text_utils import (
    default_constraints,
    default_education,
    default_preferences,
    default_skills,
)

# Invariants:
# - LLM output never writes directly to candidate_profiles
# - candidate_resumes and committed profile rows are INSERT-only
# - Every evidence row has source_resume_id
# - Exactly one is_current=true profile per candidate (transactional)


async def get_current_profile(db: AsyncSession, candidate_id: uuid.UUID) -> CandidateProfile | None:
    result = await db.execute(
        select(CandidateProfile).where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.is_current.is_(True),
        )
    )
    return result.scalar_one_or_none()


async def get_active_evidence(db: AsyncSession, candidate_id: uuid.UUID) -> list[CandidateEvidence]:
    result = await db.execute(
        select(CandidateEvidence).where(
            CandidateEvidence.candidate_id == candidate_id,
            CandidateEvidence.is_active.is_(True),
        )
    )
    return list(result.scalars().all())


async def get_pending_patch(db: AsyncSession, candidate_id: uuid.UUID) -> CandidatePatch | None:
    result = await db.execute(
        select(CandidatePatch)
        .where(
            CandidatePatch.candidate_id == candidate_id,
            CandidatePatch.status == "pending",
        )
        .order_by(CandidatePatch.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _reject_pending_patch(db: AsyncSession, patch: CandidatePatch) -> None:
    for op in patch.proposed_operations:
        if op.get("evidence_id") and op["op"] in {"ADD_EXPERIENCE", "ADD_PROJECT", "ADD_CERTIFICATION"}:
            evidence = await db.get(CandidateEvidence, uuid.UUID(op["evidence_id"]))
            if evidence and not evidence.is_approved:
                evidence.is_active = False

    patch.status = "rejected"
    patch.committed_at = datetime.now(UTC)


async def _reject_all_pending_patches(db: AsyncSession, candidate_id: uuid.UUID) -> None:
    result = await db.execute(
        select(CandidatePatch).where(
            CandidatePatch.candidate_id == candidate_id,
            CandidatePatch.status == "pending",
        )
    )
    for patch in result.scalars().all():
        await _reject_pending_patch(db, patch)


def _apply_skill_ops(ops: list[dict[str, Any]], skills: dict[str, Any]) -> dict[str, Any]:
    updated = {k: list(v) for k, v in skills.items()}
    for op in ops:
        if op["op"] != "ADD_SKILL":
            continue
        category = op["category"]
        updated.setdefault(category, [])
        if op["value"] not in updated[category]:
            updated[category].append(op["value"])
    return updated


def _apply_constraint_ops(ops: list[dict[str, Any]], constraints: dict[str, Any]) -> dict[str, Any]:
    updated = dict(constraints)
    for op in ops:
        if op["op"] == "ADD_CONSTRAINT_SUGGESTION":
            updated[op["field"]] = op["suggested_value"]
        elif op["op"] == "UPDATE_CONSTRAINT":
            updated[op["field"]] = op["to"]
    return updated


def _apply_preference_ops(ops: list[dict[str, Any]], preferences: dict[str, Any]) -> dict[str, Any]:
    updated = dict(preferences)
    for op in ops:
        if op["op"] == "ADD_PREFERENCE_SUGGESTION":
            field = op["field"]
            value = op["suggested_value"]
            if isinstance(value, list):
                existing = updated.setdefault(field, [])
                for item in value:
                    if item not in existing:
                        existing.append(item)
            else:
                updated[field] = value
        elif op["op"] == "UPDATE_PREFERENCE":
            updated[op["field"]] = op["to"]
    return updated


def _apply_education_ops(ops: list[dict[str, Any]], education: dict[str, Any]) -> dict[str, Any]:
    updated = dict(education)
    contact = dict(updated.get("contact") or {})
    entries = list(updated.get("entries") or [])

    for op in ops:
        if op["op"] == "ADD_EDUCATION":
            updated.update(op["data"])
            if "contact" in op["data"]:
                contact.update(op["data"]["contact"] or {})
            if "entries" in op["data"]:
                entries.extend(op["data"]["entries"] or [])
        elif op["op"] == "UPDATE_EDUCATION":
            updated[op["field"]] = op["to"]
        elif op["op"] == "ADD_CONTACT":
            contact.update(op["data"])
        elif op["op"] == "UPDATE_CONTACT":
            contact[op["field"]] = op["to"]
        elif op["op"] == "ADD_EDUCATION_ENTRY":
            entries.append(op["data"])
        elif op["op"] == "SET_SECTION_ORDER":
            updated["section_order"] = op["value"]

    if contact:
        updated["contact"] = contact
    if entries:
        updated["entries"] = entries
    return updated


async def _create_evidence_for_ops(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    source_resume_id: uuid.UUID,
    operations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    updated_ops: list[dict[str, Any]] = []
    for op in operations:
        op_copy = dict(op)
        if op_copy["op"] == "ADD_EXPERIENCE":
            evidence = CandidateEvidence(
                candidate_id=candidate_id,
                source_resume_id=source_resume_id,
                evidence_type="experience",
                normalized_data=op_copy["data"],
            )
            db.add(evidence)
            await db.flush()
            op_copy["evidence_id"] = str(evidence.id)
        elif op_copy["op"] == "ADD_PROJECT":
            evidence = CandidateEvidence(
                candidate_id=candidate_id,
                source_resume_id=source_resume_id,
                evidence_type="project",
                normalized_data=op_copy["data"],
            )
            db.add(evidence)
            await db.flush()
            op_copy["evidence_id"] = str(evidence.id)
        elif op_copy["op"] == "ADD_CERTIFICATION":
            evidence = CandidateEvidence(
                candidate_id=candidate_id,
                source_resume_id=source_resume_id,
                evidence_type="certification",
                normalized_data=op_copy["data"],
            )
            db.add(evidence)
            await db.flush()
            op_copy["evidence_id"] = str(evidence.id)
        updated_ops.append(op_copy)
    return updated_ops


async def process_resume_upload(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    resume: CandidateResume,
    settings: Settings,
) -> CandidatePatch:
    await db.execute(
        sql_text("SELECT pg_advisory_xact_lock(hashtext(:candidate_id))"),
        {"candidate_id": str(candidate_id)},
    )
    await _reject_all_pending_patches(db, candidate_id)

    llm_provider = get_llm_provider(settings)
    storage = get_resume_storage(settings)
    pdf_bytes = storage.read_bytes(resume.file_path)
    extracted_text, method, status = await extract_text(
        pdf_bytes,
        settings=settings,
        llm_provider=llm_provider,
    )
    resume.extraction_method = method
    resume.raw_text = extracted_text
    resume.raw_text_char_count = len(extracted_text)
    resume.extraction_status = status
    resume.parsed_at = datetime.now(UTC)

    extracted = await extract_resume_evidence(extracted_text, llm_provider)
    current_profile = await get_current_profile(db, candidate_id)
    current_evidence = await get_active_evidence(db, candidate_id)
    operations = compute_proposed_operations(extracted, current_profile, current_evidence)
    operations = await _create_evidence_for_ops(
        db,
        candidate_id=candidate_id,
        source_resume_id=resume.id,
        operations=operations,
    )

    version_before = current_profile.version if current_profile else None
    patch = CandidatePatch(
        candidate_id=candidate_id,
        source_resume_id=resume.id,
        profile_version_before=version_before,
        status="pending",
        proposed_operations=operations,
    )
    db.add(patch)
    await db.commit()
    await db.refresh(patch)
    return patch


async def commit_patch(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    patch_id: uuid.UUID,
    approved_operation_ids: list[str],
    settings: Settings,
) -> CandidateProfile:
    patch = await db.get(CandidatePatch, patch_id)
    if patch is None or patch.candidate_id != candidate_id:
        raise NotFoundError("Patch not found")
    if patch.status != "pending":
        raise ConflictError("Patch is not pending")

    approved_ids = set(approved_operation_ids)
    approved_ops = [op for op in patch.proposed_operations if op.get("id") in approved_ids]
    rejected_ops = [op for op in patch.proposed_operations if op.get("id") not in approved_ids]

    current_profile = await get_current_profile(db, candidate_id)
    if current_profile:
        skills = dict(current_profile.skills)
        constraints = dict(current_profile.constraints)
        preferences = dict(current_profile.preferences)
        education = dict(current_profile.education)
        current_version = current_profile.version
    else:
        skills = default_skills()
        constraints = default_constraints()
        preferences = default_preferences()
        education = default_education()
        current_version = 0

    skills = _apply_skill_ops(approved_ops, skills)
    constraints = _apply_constraint_ops(approved_ops, constraints)
    preferences = _apply_preference_ops(approved_ops, preferences)
    education = _apply_education_ops(approved_ops, education)

    for op in approved_ops:
        if op["op"] in {"ADD_EXPERIENCE", "ADD_PROJECT", "ADD_CERTIFICATION"}:
            evidence_id = uuid.UUID(op["evidence_id"])
            evidence = await db.get(CandidateEvidence, evidence_id)
            if evidence:
                evidence.is_approved = True
                evidence.approved_at = datetime.now(UTC)
        elif op["op"] == "UPDATE_EXPERIENCE":
            evidence = await db.get(CandidateEvidence, uuid.UUID(op["evidence_id"]))
            if evidence:
                evidence.normalized_data = {**evidence.normalized_data, op["field"]: op["to"]}
                evidence.is_approved = True
                evidence.approved_at = datetime.now(UTC)
        elif op["op"] == "UPDATE_PROJECT":
            evidence = await db.get(CandidateEvidence, uuid.UUID(op["evidence_id"]))
            if evidence:
                evidence.normalized_data = {**evidence.normalized_data, op["field"]: op["to"]}
                evidence.is_approved = True
                evidence.approved_at = datetime.now(UTC)

    for op in rejected_ops:
        if op["op"] in {"ADD_EXPERIENCE", "ADD_PROJECT", "ADD_CERTIFICATION"} and op.get("evidence_id"):
            evidence = await db.get(CandidateEvidence, uuid.UUID(op["evidence_id"]))
            if evidence:
                evidence.is_active = False

    constraints = await refresh_experience_tier_constraints(
        db,
        candidate_id=candidate_id,
        constraints=constraints,
        education=education,
    )
    constraints = normalize_constraints(constraints)

    if current_profile:
        await db.execute(
            update(CandidateProfile)
            .where(CandidateProfile.candidate_id == candidate_id, CandidateProfile.is_current.is_(True))
            .values(is_current=False)
        )

    new_version = current_version + 1
    new_profile = CandidateProfile(
        candidate_id=candidate_id,
        version=new_version,
        is_current=True,
        schema_version="v1",
        constraints=constraints,
        preferences=preferences,
        skills=skills,
        education=education,
        patch_id=patch.id,
    )
    db.add(new_profile)
    await db.flush()

    patch.status = "committed" if approved_ops else "rejected"
    if approved_ops and rejected_ops:
        patch.status = "partial"
    patch.approved_operations = approved_ops
    patch.rejected_operations = rejected_ops
    patch.profile_version_after = new_version
    patch.committed_at = datetime.now(UTC)

    await db.commit()
    await db.refresh(new_profile)

    await recompute_capabilities(db, candidate_id=candidate_id, profile_version=new_version, settings=settings)
    return new_profile


async def discard_patch(db: AsyncSession, *, candidate_id: uuid.UUID, patch_id: uuid.UUID) -> None:
    patch = await db.get(CandidatePatch, patch_id)
    if patch is None or patch.candidate_id != candidate_id:
        raise NotFoundError("Patch not found")
    if patch.status != "pending":
        raise ConflictError("Patch is not pending")

    await _reject_pending_patch(db, patch)
    await db.commit()


def _merge_constraints(constraints: dict[str, Any], new_values: dict[str, Any]) -> dict[str, Any]:
    if "eeo" in new_values and isinstance(new_values["eeo"], dict):
        merged_eeo = dict(constraints.get("eeo") or {})
        merged_eeo.update(new_values["eeo"])
        updated = {**constraints, **{k: v for k, v in new_values.items() if k != "eeo"}}
        updated["eeo"] = merged_eeo
        return updated
    return {**constraints, **new_values}


async def write_profile_filters(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    constraints_updates: dict[str, Any],
    preferences_updates: dict[str, Any],
) -> CandidateProfile:
    """Atomically update constraints and preferences without LLM capability recompute."""
    if not constraints_updates and not preferences_updates:
        raise ValueError("No filter updates provided")

    current_profile = await get_current_profile(db, candidate_id)
    if current_profile:
        constraints = dict(current_profile.constraints)
        preferences = dict(current_profile.preferences)
        education = dict(current_profile.education)
        skills = dict(current_profile.skills)
        current_version = current_profile.version
    else:
        constraints = default_constraints()
        preferences = default_preferences()
        education = default_education()
        skills = default_skills()
        current_version = 0

    if constraints_updates:
        constraints = _merge_constraints(constraints, constraints_updates)
    if preferences_updates:
        preferences = {**preferences, **preferences_updates}

    constraints = await refresh_experience_tier_constraints(
        db,
        candidate_id=candidate_id,
        constraints=constraints,
        education=education,
    )
    constraints = normalize_constraints(constraints)

    if current_profile:
        await db.execute(
            update(CandidateProfile)
            .where(CandidateProfile.candidate_id == candidate_id, CandidateProfile.is_current.is_(True))
            .values(is_current=False)
        )

    new_version = current_version + 1
    new_profile = CandidateProfile(
        candidate_id=candidate_id,
        version=new_version,
        is_current=True,
        schema_version="v1",
        constraints=constraints,
        preferences=preferences,
        skills=skills,
        education=education,
        patch_id=None,
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


async def write_profile_section(
    db: AsyncSession,
    *,
    candidate_id: uuid.UUID,
    section: str,
    new_values: dict[str, Any],
) -> CandidateProfile:
    current_profile = await get_current_profile(db, candidate_id)
    if current_profile:
        constraints = dict(current_profile.constraints)
        preferences = dict(current_profile.preferences)
        education = dict(current_profile.education)
        skills = dict(current_profile.skills)
        current_version = current_profile.version
    else:
        constraints = default_constraints()
        preferences = default_preferences()
        education = default_education()
        skills = default_skills()
        current_version = 0

    if section == "constraints":
        constraints = _merge_constraints(constraints, new_values)
    elif section == "preferences":
        preferences.update(new_values)
    elif section == "education":
        if "contact" in new_values and isinstance(new_values["contact"], dict):
            merged_contact = dict(education.get("contact") or {})
            merged_contact.update(new_values["contact"])
            education = {**education, **{k: v for k, v in new_values.items() if k != "contact"}}
            education["contact"] = merged_contact
        elif "entries" in new_values and isinstance(new_values["entries"], list):
            education = {**education, **{k: v for k, v in new_values.items() if k != "entries"}}
            education["entries"] = new_values["entries"]
        else:
            education.update(new_values)
    else:
        raise ValueError(f"Unknown section: {section}")

    constraints = await refresh_experience_tier_constraints(
        db,
        candidate_id=candidate_id,
        constraints=constraints,
        education=education,
    )
    constraints = normalize_constraints(constraints)

    if current_profile:
        await db.execute(
            update(CandidateProfile)
            .where(CandidateProfile.candidate_id == candidate_id, CandidateProfile.is_current.is_(True))
            .values(is_current=False)
        )

    new_version = current_version + 1
    new_profile = CandidateProfile(
        candidate_id=candidate_id,
        version=new_version,
        is_current=True,
        schema_version="v1",
        constraints=constraints,
        preferences=preferences,
        skills=skills,
        education=education,
        patch_id=None,
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile
