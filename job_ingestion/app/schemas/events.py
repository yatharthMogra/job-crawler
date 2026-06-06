from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class IngestionEventOut(BaseModel):
    id: str
    event_type: str
    event_category: str
    severity: str
    platform: Optional[str]
    company_id: Optional[str]
    pipeline_run_id: Optional[str]
    normalized_job_id: Optional[str]
    metadata: dict[str, Any]
    created_at: datetime


class EventSummaryOut(BaseModel):
    event_type: str
    event_category: str
    severity: str
    count: int
