class ProcessingState:
    PENDING = "pending"
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    EXTRACTION_FAILED = "extraction_failed"
    ENRICHMENT_FAILED = "enrichment_failed"
    MALFORMED_SOURCE = "malformed_source"
    REQUIRES_REVIEW = "requires_review"
    MANUALLY_CORRECTED = "manually_corrected"


class FailureReason:
    JSON_PARSE_FAILURE = "json_parse_failure"
    MALFORMED_HTML = "malformed_html"
    MISSING_REQUIRED_FIELDS = "missing_required_fields"
    LLM_TIMEOUT = "llm_timeout"
    LLM_SCHEMA_MISMATCH = "llm_schema_mismatch"
    LLM_EMPTY_RESPONSE = "llm_empty_response"
    HTTP_ERROR = "http_error"
    NETWORK_TIMEOUT = "network_timeout"
    MALFORMED_SOURCE_RESPONSE = "malformed_source_response"
    TOKEN_LIMIT_EXCEEDED = "token_limit_exceeded"
    UNSUPPORTED_PLATFORM = "unsupported_platform"
    EXTRACTION_EXCEPTION = "extraction_exception"
    EMPTY_SKILL_EXTRACTION = "empty_skill_extraction"
    STALE_POSTING = "stale_posting"


class EventType:
    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_COMPLETED = "pipeline_completed"
    PIPELINE_PARTIAL_SUCCESS = "pipeline_partial_success"
    PIPELINE_FAILED = "pipeline_failed"
    SOURCE_FETCH_FAILED = "source_fetch_failed"
    SOURCE_FAILURE_THRESHOLD_REACHED = "source_failure_threshold_reached"
    SOURCE_RECOVERED = "source_recovered"
    MALFORMED_SOURCE_RESPONSE = "malformed_source_response"
    LLM_EXTRACTION_FAILED = "llm_extraction_failed"
    MALFORMED_LLM_RESPONSE = "malformed_llm_response"
    ENRICHMENT_SKIPPED = "enrichment_skipped"
    TOKEN_SPIKE_DETECTED = "token_spike_detected"
    REVIEWER_EDITED_JOB = "reviewer_edited_job"
    REVIEWER_DISABLED_JOB = "reviewer_disabled_job"
    JOB_MARKED_REQUIRES_REVIEW = "job_marked_requires_review"
    SCHEDULER_STARTED = "scheduler_started"
    SCHEDULER_STOPPED = "scheduler_stopped"
    JOB_REJECTED_STALE = "job_rejected_stale"


class EventCategory:
    PIPELINE = "pipeline"
    SOURCE = "source"
    ENRICHMENT = "enrichment"
    REVIEW = "review"
    SYSTEM = "system"


class EventSeverity:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
