from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion"
    notification_cadence_hours: int = 24
    notification_cadence_minutes: int | None = None
    enable_notification_scheduler: bool = True
    notification_retrieval_limit: int = 500
    recommendation_retrieval_limit: int | None = None
    recommendation_pool_floor_ratio: float = 0.1
    recommendation_max_jobs_per_company: int = 5
    recommendation_company_unlock_batch: int = 5
    notification_jobs_per_email: int = 4
    notification_max_jobs_per_company: int = 1
    job_max_age_days: int = 7
    notification_min_jobs_to_send: int = 1
    digest_scheduler_poll_minutes: int = 15
    company_watch_poll_minutes: int = 3
    company_watch_batch_size: int = 50
    company_watch_max_jobs_per_email: int = 5
    company_watch_min_score: float = 0.5
    default_digest_cadence_hours: int = 24
    default_digest_top_k: int = 4
    resend_api_key: str = ""
    email_from: str = "Job Scout <notifications@job-scout.dev>"
    score_capability_weight: float = 0.40
    score_skill_weight: float = 0.25
    score_location_weight: float = 0.20
    score_compensation_weight: float = 0.15
    log_level: str = "INFO"
    cors_origins: str = ""
    app_base_url: str = "http://localhost:3000"
    domain_filter_enabled: bool = False
    role_intent_filter_enabled: bool = False
    clearance_filter_enabled: bool = False
    sponsorship_score_enabled: bool = False
    score_sponsorship_weight: float = 0.12
    score_capability_weight_with_sponsorship: float = 0.35
    score_skill_weight_with_sponsorship: float = 0.22
    score_location_weight_with_sponsorship: float = 0.18
    score_compensation_weight_with_sponsorship: float = 0.13
    experience_tier_visibility_enabled: bool = False
    experience_tier_visibility_ceiling: str = "SENIOR"
    experience_tier_score_enabled: bool = False
    score_experience_tier_weight: float = 0.15
    score_capability_weight_with_tier: float = 0.34
    score_skill_weight_with_tier: float = 0.21
    score_location_weight_with_tier: float = 0.17
    score_compensation_weight_with_tier: float = 0.13
    ats_fit_enabled: bool = False
    ats_fit_bm25_weight: float = 0.50
    ats_fit_semantic_weight: float = 0.25
    ats_fit_structural_weight: float = 0.25
    pool_percentile_refresh_enabled: bool = True
    # RRF + cache-backed pagination
    redis_url: str = ""
    recommendation_rrf_enabled: bool = True
    recommendation_rrf_k: int = 60
    recommendation_page_size: int = 40
    recommendation_page_size_max: int = 100
    recommendation_cache_ttl_seconds: int = 1800

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def _sync_retrieval_limit(self) -> "Settings":
        if self.recommendation_retrieval_limit is None:
            self.recommendation_retrieval_limit = self.notification_retrieval_limit
        return self

    @property
    def effective_retrieval_limit(self) -> int:
        return self.recommendation_retrieval_limit or self.notification_retrieval_limit

    @property
    def allowed_cors_origins(self) -> list[str]:
        defaults = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
            "http://localhost:3002",
            "http://127.0.0.1:3002",
            "https://job-scout.dev",
            "https://carrier-match-gcp.vercel.app",
        ]
        if not self.cors_origins.strip():
            return defaults
        extra = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return list(dict.fromkeys(defaults + extra))


def notification_interval_kwargs(settings: Settings) -> dict[str, int]:
    if settings.notification_cadence_minutes is not None:
        return {"minutes": settings.notification_cadence_minutes}
    return {"hours": settings.notification_cadence_hours}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
