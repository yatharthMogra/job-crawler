from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class NormalizedJob(Base):
    __tablename__ = "normalized_jobs"
    __table_args__ = (
        UniqueConstraint("company_id", "external_job_id", name="uq_normalized_jobs_company_external"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raw_jobs.id", ondelete="CASCADE"), nullable=False
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    external_job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    posting_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_preview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    posted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    consecutive_misses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    seniority: Mapped[str] = mapped_column(String(64), nullable=False, default="unclear")
    is_internship: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_new_grad: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sponsorship_status: Mapped[str] = mapped_column(String(32), nullable=False, default="unclear")
    sponsorship_confidence: Mapped[str] = mapped_column(String(16), nullable=False, default="low")
    remote_type: Mapped[str] = mapped_column(String(32), nullable=False, default="unclear")
    tech_stack: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    skills: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    llm_provider: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    llm_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    extraction_version: Mapped[str] = mapped_column(String(32), nullable=False)
    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    processing_state: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    failure_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_failure_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_manual_review_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_review_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
