from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion"
    fetch_cadence_hours: int = 6
    max_consecutive_failures_before_alert: int = 3
    consecutive_misses_before_inactive: int = 3
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"
    extraction_version: str = "v5"
    default_extraction_version: str = "v5"
    opportunity_score_freshness_decay: float = 0.01
    comp_floor: int = 40_000
    comp_ceiling: int = 250_000
    freshness_weight: float = 0.40
    compensation_weight: float = 0.40
    effort_weight: float = 0.20
    alerts_file_path: str = "./alerts.json"
    fetch_concurrency: int = 10
    token_spike_threshold: int = 8000
    enrichment_micro_batch_size: int = 16
    enrichment_window_seconds: int = 45
    enrichment_max_batches_per_window: int = 20
    enrichment_max_jobs_per_window: int = 100
    enrichment_llm_max_rpm: int = 12
    enrichment_cooldown_seconds: int = 120
    enrichment_max_retries: int = 3
    enrichment_max_input_tokens_per_batch: int = 14000
    enrichment_window_token_budget: int = 200000
    enrichment_token_estimation_strategy: str = "chars"
    llm_input_token_cost_per_1k: float = 0.0015
    llm_output_token_cost_per_1k: float = 0.002
    enrichment_stop_on_daily_quota: bool = True
    log_level: str = "INFO"
    active_job_retention_days: int = 7
    archive_retention_days: int = 100
    cleanup_batch_size: int = 500
    archive_dir: str = "data/archives"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def alerts_path(self) -> Path:
        return Path(self.alerts_file_path)

    @property
    def effort_scores(self) -> dict[str, float]:
        return {"LOW": 1.0, "MEDIUM": 0.6, "HIGH": 0.2}

    @property
    def enrichment_batch_interval_seconds(self) -> float:
        rpm_cap = max(self.enrichment_llm_max_rpm, 1)
        window_batches = min(self.enrichment_max_batches_per_window, rpm_cap)
        return self.enrichment_window_seconds / window_batches


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
