from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CandidateResume(Base):
    __tablename__ = "candidate_resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extraction_status: Mapped[str] = mapped_column(String(32), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    content_embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float), nullable=True)
    content_embedding_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    content_embedding_computed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
