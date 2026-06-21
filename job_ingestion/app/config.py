from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

FetchBackpressureMode = Literal["skip_tiers", "halt_all"]

PLATFORM_FAILURE_ALERT_THRESHOLDS: dict[str, int] = {
    "rippling": 2,
}


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion"
    fetch_schedule_json: str = ""
    fetch_backpressure_enabled: bool = True
    fetch_backpressure_queue_threshold: int = 2000
    fetch_backpressure_mode: FetchBackpressureMode = "skip_tiers"
    fetch_backpressure_skip_tiers: str = "3"
    fetch_backpressure_allow_waas: bool = True
    fetch_cadence_hours: int = 6  # deprecated: replaced by FETCH_SCHEDULE_JSON
    fetch_cadence_minutes: int | None = None  # deprecated: replaced by FETCH_SCHEDULE_JSON
    max_consecutive_failures_before_alert: int = 3
    consecutive_misses_before_inactive: int = 3
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_api_keys: str = ""
    enrichment_worker_count: int = 0
    gemini_model: str = "gemini-3.1-flash-lite"
    extraction_version: str = "v6"
    default_extraction_version: str = "v6"
    opportunity_score_freshness_decay: float = 0.01
    comp_floor: int = 40_000
    comp_ceiling: int = 250_000
    freshness_weight: float = 0.40
    compensation_weight: float = 0.40
    effort_weight: float = 0.20
    alerts_file_path: str = "./alerts.json"
    ingestion_stats_file_path: str = "exports/ingestion_stats.json"
    ingestion_stats_interval_minutes: int = 5
    token_spike_threshold: int = 8000
    enrichment_micro_batch_size: int = 12
    enrichment_window_seconds: int = 45
    enrichment_max_batches_per_window: int = 12
    enrichment_max_jobs_per_window: int = 64
    enrichment_llm_max_rpm: int = 10
    enrichment_cooldown_seconds: int = 120
    enrichment_max_retries: int = 3
    enrichment_max_input_tokens_per_batch: int = 14000
    enrichment_window_token_budget: int = 200000
    enrichment_token_estimation_strategy: str = "chars"
    llm_input_token_cost_per_1k: float = 0.0015
    llm_output_token_cost_per_1k: float = 0.002
    enrichment_stop_on_daily_quota: bool = True
    job_max_age_days: int = 7
    ashby_host_rate_per_second: float = 1.5
    ashby_host_burst: int = 3
    ashby_full_refresh_days: int = 7
    shutdown_worker_timeout_seconds: int = 30
    log_level: str = "INFO"
    archive_retention_days: int = 100
    cleanup_batch_size: int = 500
    archive_dir: str = "data/archives"

    yc_crawler_email: str = ""
    yc_crawler_password: str = ""
    yc_directory_probe_concurrency: int = 5
    yc_waas_roles: str = "eng,ds"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("fetch_backpressure_mode", mode="before")
    @classmethod
    def _validate_fetch_backpressure_mode(cls, value: object) -> str:
        normalized = str(value).strip().lower()
        if normalized not in {"skip_tiers", "halt_all"}:
            raise ValueError("FETCH_BACKPRESSURE_MODE must be 'skip_tiers' or 'halt_all'")
        return normalized

    @property
    def alerts_path(self) -> Path:
        return Path(self.alerts_file_path)

    @property
    def ingestion_stats_path(self) -> Path:
        return Path(self.ingestion_stats_file_path)

    @property
    def effort_scores(self) -> dict[str, float]:
        return {"LOW": 1.0, "MEDIUM": 0.6, "HIGH": 0.2}

    @property
    def enrichment_batch_interval_seconds(self) -> float:
        rpm_cap = max(self.enrichment_llm_max_rpm, 1)
        window_batches = min(self.enrichment_max_batches_per_window, rpm_cap)
        return self.enrichment_window_seconds / window_batches

    @property
    def yc_waas_roles_list(self) -> list[str]:
        return [role.strip() for role in self.yc_waas_roles.split(",") if role.strip()]

    def fetch_schedule(self):
        from app.ingestion.fetch_schedule_config import get_fetch_schedule

        return get_fetch_schedule(self.fetch_schedule_json)

    def fetch_backpressure_skip_tiers_set(self) -> set[int]:
        return {int(tier.strip()) for tier in self.fetch_backpressure_skip_tiers.split(",") if tier.strip()}

    def gemini_api_keys_list(self) -> list[str]:
        if self.gemini_api_keys.strip():
            keys = [key.strip() for key in self.gemini_api_keys.split(",") if key.strip()]
            if keys:
                return keys
        if self.gemini_api_key.strip():
            return [self.gemini_api_key.strip()]
        return []

    def resolved_enrichment_worker_count(self) -> int:
        keys = self.gemini_api_keys_list()
        if not keys:
            return 0
        count = self.enrichment_worker_count if self.enrichment_worker_count > 0 else len(keys)
        if count > len(keys):
            raise ValueError(
                f"ENRICHMENT_WORKER_COUNT={count} exceeds configured Gemini keys ({len(keys)})"
            )
        return count

    def worker_settings(self, gemini_api_key: str) -> Settings:
        return self.model_copy(
            update={
                "gemini_api_key": gemini_api_key,
                "enrichment_stop_on_daily_quota": False,
            }
        )

    def primary_enrichment_settings(self) -> Settings:
        keys = self.gemini_api_keys_list()
        if not keys:
            return self
        return self.worker_settings(keys[0])


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
