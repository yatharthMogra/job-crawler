from __future__ import annotations

import pytest

from app.exceptions import LLMProviderError
from app.ingestion.constants import FailureReason
from app.ingestion.gemini_error_log import (
    FAILURE_STAGE_API,
    FAILURE_STAGE_OTHER,
    FAILURE_STAGE_PARSE,
    classify_failure_stage,
    resolve_batch_assigned_failure_reason,
)


def test_classify_failure_stage_api_error() -> None:
    exc = LLMProviderError("Gemini completion failed: 429 RESOURCE_EXHAUSTED")
    assert classify_failure_stage(exc) == FAILURE_STAGE_API


def test_classify_failure_stage_parse_error() -> None:
    exc = ValueError("Failed to parse batch enrichment response: invalid json")
    assert classify_failure_stage(exc) == FAILURE_STAGE_PARSE


def test_classify_failure_stage_other() -> None:
    exc = NameError("update_job_archive_after_enrichment is not defined")
    assert classify_failure_stage(exc) == FAILURE_STAGE_OTHER


def test_resolve_batch_assigned_failure_reason_capacity() -> None:
    assert (
        resolve_batch_assigned_failure_reason(
            provider_capacity=True,
            daily_quota=False,
            schema_error=False,
            stop_on_daily_quota=True,
        )
        == FailureReason.TOKEN_LIMIT_EXCEEDED
    )


def test_resolve_batch_assigned_failure_reason_schema() -> None:
    assert (
        resolve_batch_assigned_failure_reason(
            provider_capacity=False,
            daily_quota=False,
            schema_error=True,
            stop_on_daily_quota=True,
        )
        == FailureReason.LLM_SCHEMA_MISMATCH
    )
