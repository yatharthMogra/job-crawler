from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion"
    notification_cadence_hours: int = 3
    notification_retrieval_limit: int = 50
    notification_jobs_per_email: int = 4
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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
