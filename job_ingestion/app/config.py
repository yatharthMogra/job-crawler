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
    extraction_version: str = "v2"
    default_extraction_version: str = "v2"
    opportunity_score_freshness_decay: float = 0.01
    comp_floor: int = 40_000
    comp_ceiling: int = 250_000
    freshness_weight: float = 0.40
    compensation_weight: float = 0.40
    effort_weight: float = 0.20
    alerts_file_path: str = "./alerts.json"
    fetch_concurrency: int = 10
    token_spike_threshold: int = 8000
    enrichment_micro_batch_size: int = 5
    enrichment_window_seconds: int = 60
    enrichment_max_batches_per_window: int = 15
    enrichment_max_jobs_per_window: int = 75
    enrichment_cooldown_seconds: int = 120
    enrichment_max_retries: int = 3
    enrichment_max_input_tokens_per_batch: int = 12000
    enrichment_window_token_budget: int = 200000
    enrichment_token_estimation_strategy: str = "count_tokens"
    llm_input_token_cost_per_1k: float = 0.0015
    llm_output_token_cost_per_1k: float = 0.002
    log_level: str = "INFO"

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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
