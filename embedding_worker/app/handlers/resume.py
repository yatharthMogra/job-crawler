from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.embeddings.service import embed_text, embedding_model_name
from app.models.resume import CandidateResume

log = structlog.get_logger(__name__)


class ResumeEmbedOutcome(str, Enum):
    UPDATED = "updated"
    SKIPPED = "skipped"
    NOT_FOUND = "not_found"
    TRANSIENT_ERROR = "transient_error"


async def process_resume_embedding(resume_id: uuid.UUID) -> ResumeEmbedOutcome:
    async with AsyncSessionLocal() as db:
        return await _process_resume_embedding(db, resume_id)


async def _process_resume_embedding(db: AsyncSession, resume_id: uuid.UUID) -> ResumeEmbedOutcome:
    resume = await db.get(CandidateResume, resume_id)
    if resume is None:
        log.info("resume_embedding_skipped", resume_id=str(resume_id), reason="not_found")
        return ResumeEmbedOutcome.NOT_FOUND

    if resume.content_embedding is not None:
        log.info("resume_embedding_skipped", resume_id=str(resume_id), reason="already_embedded")
        return ResumeEmbedOutcome.SKIPPED

    if resume.extraction_status != "success":
        log.info(
            "resume_embedding_skipped",
            resume_id=str(resume_id),
            reason="extraction_not_success",
            extraction_status=resume.extraction_status,
        )
        return ResumeEmbedOutcome.SKIPPED

    raw_text = (resume.raw_text or "").strip()
    if not raw_text:
        log.info("resume_embedding_skipped", resume_id=str(resume_id), reason="empty_text")
        return ResumeEmbedOutcome.SKIPPED

    embedding = embed_text(raw_text)
    if embedding is None:
        log.warning("resume_embedding_failed", resume_id=str(resume_id), reason="embed_returned_none")
        return ResumeEmbedOutcome.TRANSIENT_ERROR

    resume.content_embedding = embedding
    resume.content_embedding_model = embedding_model_name()
    resume.content_embedding_computed_at = datetime.now(UTC)
    await db.commit()
    log.info("resume_embedding_updated", resume_id=str(resume_id))
    return ResumeEmbedOutcome.UPDATED
