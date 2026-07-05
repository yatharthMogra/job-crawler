from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import LLMProviderError
from app.ingestion.constants import FailureReason
from app.models.gemini_error import GeminiError

FAILURE_STAGE_API = "api_error"
FAILURE_STAGE_PARSE = "response_parse_error"
FAILURE_STAGE_OTHER = "other"


def _is_schema_validation_error(message: str) -> bool:
    lowered = message.lower()
    return any(
        term in lowered
        for term in [
            "validation error",
            "input should be",
            "failed to parse batch enrichment",
            "jsondecodeerror",
            "invalid json",
            "model_validate",
        ]
    )


def classify_failure_stage(exc: BaseException) -> str:
    if isinstance(exc, LLMProviderError):
        return FAILURE_STAGE_API
    if _is_schema_validation_error(str(exc)):
        return FAILURE_STAGE_PARSE
    return FAILURE_STAGE_OTHER


def resolve_batch_assigned_failure_reason(
    *,
    provider_capacity: bool,
    daily_quota: bool,
    schema_error: bool,
    stop_on_daily_quota: bool,
) -> str:
    if provider_capacity or (daily_quota and stop_on_daily_quota):
        return FailureReason.TOKEN_LIMIT_EXCEEDED
    if schema_error:
        return FailureReason.LLM_SCHEMA_MISMATCH
    return FailureReason.LLM_SCHEMA_MISMATCH


async def record_gemini_error(
    db: AsyncSession,
    *,
    exc: BaseException,
    assigned_failure_reason: str,
    call_site: str,
    llm_provider: str | None = None,
    llm_model: str | None = None,
    enrichment_batch_id: UUID | None = None,
    company_id: UUID | None = None,
    normalized_job_ids: list[UUID] | None = None,
    batch_size: int | None = None,
    source: str | None = None,
) -> Optional[GeminiError]:
    failure_stage = classify_failure_stage(exc)
    if failure_stage == FAILURE_STAGE_OTHER:
        return None

    job_ids = [str(job_id) for job_id in (normalized_job_ids or [])]
    row = GeminiError(
        assigned_failure_reason=assigned_failure_reason,
        error_message=str(exc),
        exception_type=type(exc).__name__,
        failure_stage=failure_stage,
        call_site=call_site,
        llm_provider=llm_provider,
        llm_model=llm_model,
        enrichment_batch_id=enrichment_batch_id,
        company_id=company_id,
        normalized_job_ids=job_ids,
        batch_size=batch_size,
        source=source,
    )
    db.add(row)
    return row
