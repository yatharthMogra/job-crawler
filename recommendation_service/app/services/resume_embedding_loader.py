"""Load up to 5 resume embeddings for a candidate (max-of-5 semantic signal)."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared import CandidateResume

MAX_RESUME_EMBEDDINGS = 5


@dataclass
class ResumeEmbeddingBundle:
    embeddings: list[list[float]]
    fingerprint: str
    latest_resume_id: uuid.UUID | None = None
    latest_raw_text: str | None = None


async def load_resume_embeddings(
    db: AsyncSession,
    candidate_id: uuid.UUID,
    *,
    limit: int = MAX_RESUME_EMBEDDINGS,
) -> ResumeEmbeddingBundle:
    rows = list(
        (
            await db.scalars(
                select(CandidateResume)
                .where(
                    CandidateResume.candidate_id == candidate_id,
                    CandidateResume.extraction_status == "success",
                    CandidateResume.content_embedding.is_not(None),
                )
                .order_by(CandidateResume.uploaded_at.desc())
                .limit(limit)
            )
        ).all()
    )
    embeddings = [list(row.content_embedding) for row in rows if row.content_embedding]
    fingerprint = _fingerprint(rows)
    latest = rows[0] if rows else None
    latest_raw_text = latest.raw_text if latest else None
    if not latest_raw_text:
        text_row = await db.scalar(
            select(CandidateResume)
            .where(
                CandidateResume.candidate_id == candidate_id,
                CandidateResume.extraction_status == "success",
                CandidateResume.raw_text.is_not(None),
            )
            .order_by(CandidateResume.uploaded_at.desc())
            .limit(1)
        )
        if text_row is not None:
            latest = text_row
            latest_raw_text = text_row.raw_text
    return ResumeEmbeddingBundle(
        embeddings=embeddings,
        fingerprint=fingerprint,
        latest_resume_id=latest.id if latest else None,
        latest_raw_text=latest_raw_text,
    )


async def load_resume_fingerprint(db: AsyncSession, candidate_id: uuid.UUID) -> str:
    rows = list(
        (
            await db.scalars(
                select(CandidateResume)
                .where(
                    CandidateResume.candidate_id == candidate_id,
                    CandidateResume.extraction_status == "success",
                    CandidateResume.content_embedding.is_not(None),
                )
                .order_by(CandidateResume.uploaded_at.desc())
                .limit(MAX_RESUME_EMBEDDINGS)
            )
        ).all()
    )
    return _fingerprint(rows)


def _fingerprint(rows: list[CandidateResume]) -> str:
    parts: list[str] = []
    for row in rows:
        computed = row.content_embedding_computed_at
        ts = computed.isoformat() if isinstance(computed, datetime) else ""
        parts.append(f"{row.id}:{ts}")
    raw = "|".join(parts) if parts else "none"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]
