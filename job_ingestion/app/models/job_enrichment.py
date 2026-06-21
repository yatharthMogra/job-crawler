from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobEnrichment(Base):
    __tablename__ = "job_enrichments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    normalized_job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("normalized_jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    raw_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raw_jobs.id", ondelete="SET NULL"), nullable=True
    )
    enrichment_batch_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("enrichment_batches.id", ondelete="SET NULL"), nullable=True, index=True
    )
    llm_provider: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    llm_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    extraction_version: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    seniority: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_internship: Mapped[Optional[bool]] = mapped_column(nullable=True)
    is_new_grad: Mapped[Optional[bool]] = mapped_column(nullable=True)
    sponsorship_status: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    sponsorship_confidence: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    remote_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    tech_stack: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    skills: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    normalized_roles: Mapped[list[str]] = mapped_column(ARRAY(String(64)), nullable=False, default=list)
    job_capabilities: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    application_effort: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    retrieval_pools: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False, default=list)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    opportunity_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    opportunity_score_computed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    responsibilities: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False, default=list)
    required_qualifications: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False, default=list)
    preferred_qualifications: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False, default=list)
    benefits: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False, default=list)
    input_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
