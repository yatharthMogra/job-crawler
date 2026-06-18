from __future__ import annotations

import uuid
from pathlib import Path

import structlog
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_api_key
from app.config import Settings, get_settings
from app.database import get_db
from app.exceptions import ConflictError, ExtractionError, LLMProviderError, NotFoundError
from app.models.candidate import Candidate
from app.models.resume import CandidateResume
from app.pipeline.patch_engine import process_resume_upload
from app.services.domain_sync import sync_candidate_domains
from app.schemas.candidate import (
    CandidateCreate,
    CandidateOAuthCreate,
    CandidateResponse,
    ResumeLabelUpdate,
    ResumeResponse,
    ResumeUploadResponse,
)

router = APIRouter(prefix="/candidates", tags=["candidates"], dependencies=[Depends(require_api_key)])
log = structlog.get_logger(__name__)


async def _get_candidate_or_404(db: AsyncSession, candidate_id: uuid.UUID) -> Candidate:
    candidate = await db.get(Candidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


@router.get("/lookup", response_model=CandidateResponse)
async def lookup_candidate(email: str, db: AsyncSession = Depends(get_db)) -> Candidate:
    result = await db.execute(select(Candidate).where(Candidate.email == email))
    candidate = result.scalar_one_or_none()
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


@router.post("/oauth", response_model=CandidateResponse)
async def upsert_oauth_candidate(payload: CandidateOAuthCreate, db: AsyncSession = Depends(get_db)) -> Candidate:
    result = await db.execute(select(Candidate).where(Candidate.google_sub == payload.google_sub))
    candidate = result.scalar_one_or_none()

    if candidate is None:
        result = await db.execute(select(Candidate).where(Candidate.email == payload.email))
        candidate = result.scalar_one_or_none()

    if candidate is None:
        candidate = Candidate(
            email=payload.email,
            name=payload.name,
            google_sub=payload.google_sub,
            avatar_url=payload.avatar_url,
            email_verified=payload.email_verified,
        )
        db.add(candidate)
    else:
        candidate.name = payload.name or candidate.name
        candidate.google_sub = payload.google_sub
        candidate.avatar_url = payload.avatar_url or candidate.avatar_url
        candidate.email_verified = payload.email_verified or candidate.email_verified

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists") from exc
    await db.refresh(candidate)
    return candidate


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(payload: CandidateCreate, db: AsyncSession = Depends(get_db)) -> Candidate:
    candidate = Candidate(email=payload.email, name=payload.name)
    db.add(candidate)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists") from exc
    await db.refresh(candidate)
    return candidate


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Candidate:
    return await _get_candidate_or_404(db, candidate_id)


@router.post("/{candidate_id}/resumes/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    candidate_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ResumeUploadResponse:
    await _get_candidate_or_404(db, candidate_id)
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are accepted")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File exceeds 5MB limit")

    resume_id = uuid.uuid4()
    storage_dir = settings.resume_storage_dir / str(candidate_id)
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / f"{resume_id}.pdf"
    Path(file_path).write_bytes(content)

    resume = CandidateResume(
        id=resume_id,
        candidate_id=candidate_id,
        file_path=str(file_path),
        original_filename=file.filename,
        file_size_bytes=len(content),
        extraction_status="pending",
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    try:
        patch = await process_resume_upload(db, candidate_id=candidate_id, resume=resume, settings=settings)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ExtractionError as exc:
        log.warning(
            "resume_extraction_failed",
            candidate_id=str(candidate_id),
            resume_id=str(resume.id),
            filename=file.filename,
            error=str(exc),
        )
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except LLMProviderError as exc:
        log.error(
            "resume_llm_failed",
            candidate_id=str(candidate_id),
            resume_id=str(resume.id),
            filename=file.filename,
            error=str(exc),
        )
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except Exception as exc:
        log.exception(
            "resume_upload_failed",
            candidate_id=str(candidate_id),
            resume_id=str(resume.id),
            filename=file.filename,
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    await db.refresh(resume)
    return ResumeUploadResponse(resume=ResumeResponse.model_validate(resume), patch_id=patch.id)


@router.get("/{candidate_id}/resumes", response_model=list[ResumeResponse])
async def list_resumes(candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[ResumeResponse]:
    await _get_candidate_or_404(db, candidate_id)
    result = await db.execute(
        select(CandidateResume)
        .where(CandidateResume.candidate_id == candidate_id)
        .order_by(CandidateResume.uploaded_at.desc())
    )
    return [ResumeResponse.model_validate(row) for row in result.scalars().all()]


@router.get("/{candidate_id}/resumes/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    candidate_id: uuid.UUID,
    resume_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ResumeResponse:
    await _get_candidate_or_404(db, candidate_id)
    resume = await db.get(CandidateResume, resume_id)
    if resume is None or resume.candidate_id != candidate_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return ResumeResponse.model_validate(resume)


@router.patch("/{candidate_id}/resumes/{resume_id}", response_model=ResumeResponse)
async def update_resume_label(
    candidate_id: uuid.UUID,
    resume_id: uuid.UUID,
    payload: ResumeLabelUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResumeResponse:
    await _get_candidate_or_404(db, candidate_id)
    resume = await db.get(CandidateResume, resume_id)
    if resume is None or resume.candidate_id != candidate_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    resume.display_label = payload.display_label
    await db.commit()
    await db.refresh(resume)
    return ResumeResponse.model_validate(resume)


@router.post("/{candidate_id}/recalculate-domains")
async def recalculate_domains(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str | None]:
    await _get_candidate_or_404(db, candidate_id)
    result = await sync_candidate_domains(db, candidate_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    primary_domain, secondary_domain = result
    return {"primary_domain": primary_domain, "secondary_domain": secondary_domain}
