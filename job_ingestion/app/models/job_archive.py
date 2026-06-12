from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobArchive(Base):
    __tablename__ = "job_archive"
    __table_args__ = (
        UniqueConstraint("external_job_id", "company_id", name="uq_job_archive_external_company"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    posting_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    original_posted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    seniority: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    normalized_roles: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(64)), nullable=True)
    job_capabilities: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(128)), nullable=True)
    skills: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(128)), nullable=True)
    tech_stack: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(128)), nullable=True)
    remote_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    job_domain: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    job_secondary_domain: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    description_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
