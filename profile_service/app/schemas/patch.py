from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PatchCommitRequest(BaseModel):
    approved_operation_ids: list[str] = Field(default_factory=list)


class PatchOperationResponse(BaseModel):
    id: str
    op: str
    category: str | None = None
    value: str | None = None
    evidence_id: str | None = None
    field: str | None = None
    from_value: Any = Field(default=None, alias="from")
    to: Any = None
    suggested_value: Any = None
    data: dict[str, Any] | None = None
    reason: str | None = None

    model_config = {"populate_by_name": True}


class PendingPatchResponse(BaseModel):
    patch_id: uuid.UUID
    candidate_id: uuid.UUID
    source_resume_id: uuid.UUID
    profile_version_before: int | None
    status: str
    created_at: datetime
    skills: list[PatchOperationResponse] = Field(default_factory=list)
    experiences: list[PatchOperationResponse] = Field(default_factory=list)
    projects: list[PatchOperationResponse] = Field(default_factory=list)
    certifications: list[PatchOperationResponse] = Field(default_factory=list)
    education: list[PatchOperationResponse] = Field(default_factory=list)
    constraints: list[PatchOperationResponse] = Field(default_factory=list)
    preferences: list[PatchOperationResponse] = Field(default_factory=list)


class PatchCommitResponse(BaseModel):
    patch_id: uuid.UUID
    profile_version: int
    status: str
