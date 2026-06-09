from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.evidence import CandidateEvidence
    from app.models.patch import CandidatePatch


class CandidateResume(Base):
    __tablename__ = "candidate_resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    extraction_method: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_text_char_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    extraction_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    parsed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    display_label: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    candidate: Mapped["Candidate"] = relationship(back_populates="resumes")
    evidence: Mapped[list["CandidateEvidence"]] = relationship(back_populates="source_resume")
    patches: Mapped[list["CandidatePatch"]] = relationship(back_populates="source_resume")
