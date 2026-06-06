from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


PipelineRunStatus = Literal["running", "completed", "partial_success", "failed"]


class PipelineRunOut(BaseModel):
    id: str
    run_type: str
    status: PipelineRunStatus
    started_at: str
    completed_at: Optional[str]
    total_companies: int
    successful_companies: int
    failed_companies: int
    jobs_fetched: int
    jobs_new: int
    jobs_updated: int
    jobs_unchanged: int
    jobs_removed: int


class TriggerPipelineOut(BaseModel):
    run_id: str
    status: PipelineRunStatus
    total_companies: int
    successful_companies: int
    failed_companies: int
    jobs_fetched: int
    jobs_new: int
    jobs_updated: int
    jobs_unchanged: int
    jobs_removed: int
