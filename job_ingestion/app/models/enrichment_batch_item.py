from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EnrichmentBatchItem(Base):
    __tablename__ = "enrichment_batch_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("enrichment_batches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    queue_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("enrichment_queue.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    normalized_job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("normalized_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    priority_bucket: Mapped[str] = mapped_column(String(32), nullable=False, default="first_attempt")
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    estimated_input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    actual_input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    actual_output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
