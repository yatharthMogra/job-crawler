from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ProfileResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    version: int
    is_current: bool
    schema_version: str
    constraints: dict[str, Any]
    preferences: dict[str, Any]
    skills: dict[str, Any]
    education: dict[str, Any]
    patch_id: uuid.UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ProfileVersionSummary(BaseModel):
    version: int
    is_current: bool
    created_at: datetime
    patch_id: uuid.UUID | None

    model_config = {"from_attributes": True}


class ConstraintsUpdate(BaseModel):
    sponsorship_required: bool | None = None
    visa_type: str | None = None
    work_authorization: str | None = None
    internship_only: bool | None = None
    fulltime_only: bool | None = None
    minimum_salary: float | None = None
    minimum_hourly_rate: float | None = None
    has_clearance: bool | None = None
    exclude_security_clearance: bool | None = None
    exclude_us_citizen_only: bool | None = None
    target_seniority: list[str] | None = None
    eeo: dict[str, Any] | None = None


class PreferencesUpdate(BaseModel):
    primary_roles: list[str] | None = None
    secondary_roles: list[str] | None = None
    role_pool_ids: list[str] | None = None
    preferred_locations: list[str] | None = None
    preferred_countries: list[str] | None = None
    preferred_states: list[str] | None = None
    preferred_cities: list[str] | None = None
    acceptable_locations: list[str] | None = None
    remote_preference: str | None = None
    relocation_allowed: bool | None = None
    preferred_company_stages: list[str] | None = None
    preferred_industries: list[str] | None = None
    excluded_industries: list[str] | None = None
    preferred_skills: list[str] | None = None
    excluded_skills: list[str] | None = None
    work_models: list[str] | None = None
    experience_levels: list[str] | None = None
    min_years_experience: float | None = None
    max_job_age_days: int | None = None
    role_type: str | None = None
    role_intents: list[str] | None = None
    primary_role_intents: list[str] | None = None


class EducationContactUpdate(BaseModel):
    location: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None


class EducationEntryUpdate(BaseModel):
    level: str
    degree: str | None = None
    university: str | None = None
    graduation_date: str | None = None
    gpa: str | None = None


class EducationUpdate(BaseModel):
    degree: str | None = None
    university: str | None = None
    graduation_date: str | None = None
    gpa: str | None = None
    contact: EducationContactUpdate | None = None
    entries: list[EducationEntryUpdate] | None = None


class CapabilityResponse(BaseModel):
    capability_name: str
    supporting_evidence: list[str]
    profile_version: int
    taxonomy_version: str
    computed_at: datetime

    model_config = {"from_attributes": True}


class CapabilitiesListResponse(BaseModel):
    capabilities: list[CapabilityResponse]


class EvidenceResponse(BaseModel):
    id: uuid.UUID
    evidence_type: str
    normalized_data: dict[str, Any]
    source_resume_id: uuid.UUID
    is_approved: bool
    approved_at: datetime | None

    model_config = {"from_attributes": True}


class EvidenceListResponse(BaseModel):
    evidence: list[EvidenceResponse]
