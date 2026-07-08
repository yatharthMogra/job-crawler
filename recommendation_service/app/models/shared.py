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
    plan_tier: Mapped[str] = mapped_column(String(16), nullable=False, default="free")
    plan_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
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
    primary_domain: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    secondary_domain: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
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
    job_archive_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    external_job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    job_country: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    posting_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_preview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    posted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reference_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    processing_state: Mapped[str] = mapped_column(String(32), nullable=False)
    seniority: Mapped[str] = mapped_column(String(64), nullable=False)
    experience_tier: Mapped[str] = mapped_column(String(32), nullable=False, default="UNKNOWN")
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
    job_domain: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    job_secondary_domain: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    requires_clearance: Mapped[bool] = mapped_column(Boolean, nullable=False)
    requires_citizenship: Mapped[bool] = mapped_column(Boolean, nullable=False)
    role_intent: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    opportunity_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    responsibilities: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False)
    required_qualifications: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False)
    preferred_qualifications: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False)
    benefits: Mapped[list[str]] = mapped_column(ARRAY(String(512)), nullable=False)


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[str] = mapped_column(String(64), nullable=False)
    board_token: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    logo_domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    logo_status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    logo_fetched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class CompanyEnrichment(Base):
    __tablename__ = "company_enrichments"

    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    headquarters: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    employee_count_range: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    one_line_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    glassdoor_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


class JobArchive(Base):
    __tablename__ = "job_archive"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    external_job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    posting_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    seniority: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    skills: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(128)), nullable=True)
    tech_stack: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(128)), nullable=True)
    description_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class UserApplication(Base):
    __tablename__ = "user_applications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    job_archive_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("job_archive.id", ondelete="SET NULL"), nullable=True
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    job_title: Mapped[str] = mapped_column(String(512), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    platform: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    external_job_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class H1bCompanyPoolSummary(Base):
    __tablename__ = "h1b_company_pool_summary"

    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    pool_family: Mapped[str] = mapped_column(String(50), primary_key=True)
    years_covered: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    latest_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_lca_3yr: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_h1b_3yr: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    approval_rate_3yr: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_top_sponsor: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
