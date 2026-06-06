from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RawJob(Base):
    __tablename__ = "raw_jobs"
    __table_args__ = (Index("ix_raw_jobs_company_external", "company_id", "external_job_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    external_job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[str] = mapped_column(String(64), nullable=False, default="greenhouse")
    raw_api_response: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    raw_html: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    fetch_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
