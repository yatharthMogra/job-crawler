from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=255)


class CandidateResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResumeResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    file_path: str
    original_filename: str
    file_size_bytes: int
    extraction_method: str | None
    raw_text_char_count: int | None
    extraction_status: str
    uploaded_at: datetime
    parsed_at: datetime | None

    model_config = {"from_attributes": True}


class ResumeUploadResponse(BaseModel):
    resume: ResumeResponse
    patch_id: uuid.UUID
