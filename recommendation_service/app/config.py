from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion"
    notification_cadence_hours: int = 24
    notification_cadence_minutes: int | None = None
    enable_notification_scheduler: bool = True
    notification_retrieval_limit: int = 500
    notification_jobs_per_email: int = 4
    notification_max_jobs_per_company: int = 1
    job_max_age_days: int = 7
    notification_min_jobs_to_send: int = 3
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_use_tls: bool = True
    smtp_username: str = ""
    smtp_password: str = ""
    email_from: str = "Career Match AI <noreply@example.com>"
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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def allowed_cors_origins(self) -> list[str]:
        defaults = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
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
