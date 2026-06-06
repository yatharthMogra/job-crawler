from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_api_key
from app.config import Settings, get_settings
from app.database import get_db
from app.exceptions import ConflictError, NotFoundError
from app.models.evidence import CandidateEvidence
from app.models.profile import CandidateProfile
from app.pipeline.patch_engine import (
    commit_patch,
    discard_patch,
    get_current_profile,
    get_pending_patch,
    write_profile_section,
)
from app.schemas.patch import PatchCommitRequest, PatchCommitResponse, PendingPatchResponse
from app.schemas.patch_builder import build_pending_patch_response
from app.schemas.profile import (
    CapabilitiesListResponse,
    CapabilityResponse,
    ConstraintsUpdate,
    EducationUpdate,
    EvidenceListResponse,
    EvidenceResponse,
    PreferencesUpdate,
    ProfileResponse,
    ProfileVersionSummary,
)
from app.models.capability import CandidateCapability

router = APIRouter(prefix="/candidates/{candidate_id}", tags=["profiles"], dependencies=[Depends(require_api_key)])


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> ProfileResponse:
    profile = await get_current_profile(db, candidate_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return ProfileResponse.model_validate(profile)


@router.get("/profile/versions", response_model=list[ProfileVersionSummary])
async def list_profile_versions(
    candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[ProfileVersionSummary]:
    result = await db.execute(
        select(CandidateProfile)
        .where(CandidateProfile.candidate_id == candidate_id)
        .order_by(CandidateProfile.version.desc())
    )
    return [ProfileVersionSummary.model_validate(row) for row in result.scalars().all()]


@router.get("/profile/versions/{version}", response_model=ProfileResponse)
async def get_profile_version(
    candidate_id: uuid.UUID,
    version: int,
    db: AsyncSession = Depends(get_db),
) -> ProfileResponse:
    result = await db.execute(
        select(CandidateProfile).where(
            CandidateProfile.candidate_id == candidate_id,
            CandidateProfile.version == version,
        )
    )
    profile = result.scalar_one_or_none()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile version not found")
    return ProfileResponse.model_validate(profile)


@router.get("/patches/pending", response_model=PendingPatchResponse)
async def get_pending_patch_endpoint(
    candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> PendingPatchResponse:
    patch = await get_pending_patch(db, candidate_id)
    if patch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pending patch")
    return build_pending_patch_response(patch)


@router.post("/patches/{patch_id}/commit", response_model=PatchCommitResponse)
async def commit_patch_endpoint(
    candidate_id: uuid.UUID,
    patch_id: uuid.UUID,
    payload: PatchCommitRequest,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> PatchCommitResponse:
    try:
        profile = await commit_patch(
            db,
            candidate_id=candidate_id,
            patch_id=patch_id,
            approved_operation_ids=payload.approved_operation_ids,
            settings=settings,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    from app.models.patch import CandidatePatch

    committed_patch = await db.get(CandidatePatch, patch_id)
    status_value = committed_patch.status if committed_patch else "committed"
    return PatchCommitResponse(patch_id=patch_id, profile_version=profile.version, status=status_value)


@router.delete("/patches/{patch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def discard_patch_endpoint(
    candidate_id: uuid.UUID,
    patch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    try:
        await discard_patch(db, candidate_id=candidate_id, patch_id=patch_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/evidence", response_model=EvidenceListResponse)
async def list_evidence(
    candidate_id: uuid.UUID,
    approved_only: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
) -> EvidenceListResponse:
    query = select(CandidateEvidence).where(
        CandidateEvidence.candidate_id == candidate_id,
        CandidateEvidence.is_active.is_(True),
    )
    if approved_only:
        query = query.where(CandidateEvidence.is_approved.is_(True))
    result = await db.execute(query.order_by(CandidateEvidence.created_at.desc()))
    rows = [EvidenceResponse.model_validate(row) for row in result.scalars().all()]
    return EvidenceListResponse(evidence=rows)


@router.get("/capabilities", response_model=CapabilitiesListResponse)
async def get_capabilities(
    candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> CapabilitiesListResponse:
    profile = await get_current_profile(db, candidate_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    result = await db.execute(
        select(CandidateCapability)
        .where(
            CandidateCapability.candidate_id == candidate_id,
            CandidateCapability.profile_version == profile.version,
        )
        .order_by(CandidateCapability.capability_name)
    )
    caps = [CapabilityResponse.model_validate(row) for row in result.scalars().all()]
    return CapabilitiesListResponse(capabilities=caps)


@router.patch("/profile/constraints", response_model=ProfileResponse)
async def patch_constraints(
    candidate_id: uuid.UUID,
    payload: ConstraintsUpdate,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ProfileResponse:
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No updates provided")
    profile = await write_profile_section(
        db, candidate_id=candidate_id, section="constraints", new_values=updates, settings=settings
    )
    return ProfileResponse.model_validate(profile)


@router.patch("/profile/preferences", response_model=ProfileResponse)
async def patch_preferences(
    candidate_id: uuid.UUID,
    payload: PreferencesUpdate,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ProfileResponse:
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No updates provided")
    profile = await write_profile_section(
        db, candidate_id=candidate_id, section="preferences", new_values=updates, settings=settings
    )
    return ProfileResponse.model_validate(profile)


@router.patch("/profile/education", response_model=ProfileResponse)
async def patch_education(
    candidate_id: uuid.UUID,
    payload: EducationUpdate,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ProfileResponse:
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No updates provided")
    profile = await write_profile_section(
        db, candidate_id=candidate_id, section="education", new_values=updates, settings=settings
    )
    return ProfileResponse.model_validate(profile)
