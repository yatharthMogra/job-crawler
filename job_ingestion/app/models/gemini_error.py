from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GeminiError(Base):
    __tablename__ = "gemini_errors"
    __table_args__ = (
        Index("ix_gemini_errors_assigned_failure_reason_created_at", "assigned_failure_reason", "created_at"),
        Index("ix_gemini_errors_failure_stage_created_at", "failure_stage", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assigned_failure_reason: Mapped[str] = mapped_column(String(64), nullable=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=False)
    exception_type: Mapped[str] = mapped_column(String(128), nullable=False)
    failure_stage: Mapped[str] = mapped_column(String(32), nullable=False)
    call_site: Mapped[str] = mapped_column(String(64), nullable=False)
    llm_provider: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    llm_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    enrichment_batch_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("enrichment_batches.id", ondelete="SET NULL"),
        nullable=True,
    )
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True,
    )
    normalized_job_ids: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    batch_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    error_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
