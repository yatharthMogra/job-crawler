from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EnrichmentBatch(Base):
    __tablename__ = "enrichment_batches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pipeline_runs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="worker")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="running", index=True)
    jobs_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    jobs_first_attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    jobs_retry: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    actual_input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    actual_output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
