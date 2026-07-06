from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class NotificationPreferences(Base):
    __tablename__ = "notification_preferences"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), primary_key=True
    )
    digest_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    company_watch_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cadence_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    top_k: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    digest_filters: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    last_digest_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_digest_due_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    company_watch_cadence_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=360)
    max_emails_per_day: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    last_company_watch_batch_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_company_watch_due_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
