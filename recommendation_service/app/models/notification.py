from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class NotificationBatch(Base):
    __tablename__ = "notification_batches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    jobs_in_pools: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    jobs_after_filter: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    jobs_new_since_last: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    jobs_ranked: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    jobs_sent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    skip_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="digest")
    email_delivered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class NotificationJobHistory(Base):
    __tablename__ = "notification_job_history"
    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "job_id",
            "channel",
            name="uq_notification_job_history_candidate_job_channel",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("notification_batches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("normalized_jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    rank_in_batch: Mapped[int] = mapped_column(Integer, nullable=False)
    recommendation_score: Mapped[float] = mapped_column(Float, nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="digest")
    explanation: Mapped[list[str]] = mapped_column(ARRAY(String(256)), nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
