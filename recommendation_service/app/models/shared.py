"""Read-only models for tables owned by other services."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False)
    schema_version: Mapped[str] = mapped_column(String(16), nullable=False)
    constraints: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    preferences: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    skills: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    education: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CandidateCapability(Base):
    __tablename__ = "candidate_capabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    profile_version: Mapped[int] = mapped_column(Integer, nullable=False)
    taxonomy_version: Mapped[str] = mapped_column(String(16), nullable=False)
    capability_name: Mapped[str] = mapped_column(String(128), nullable=False)
    supporting_evidence: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CandidateEvidence(Base):
    __tablename__ = "candidate_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(32), nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    normalized_data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)


class NormalizedJob(Base):
    __tablename__ = "normalized_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    posting_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    posted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    processing_state: Mapped[str] = mapped_column(String(32), nullable=False)
    seniority: Mapped[str] = mapped_column(String(64), nullable=False)
    is_internship: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_new_grad: Mapped[bool] = mapped_column(Boolean, nullable=False)
    sponsorship_status: Mapped[str] = mapped_column(String(32), nullable=False)
    sponsorship_confidence: Mapped[str] = mapped_column(String(16), nullable=False)
    remote_type: Mapped[str] = mapped_column(String(32), nullable=False)
    tech_stack: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False)
    skills: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False)
    normalized_roles: Mapped[list[str]] = mapped_column(ARRAY(String(64)), nullable=False)
    job_capabilities: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False)
    application_effort: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    retrieval_pools: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    opportunity_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
