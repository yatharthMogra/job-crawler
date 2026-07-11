from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion"
    api_key: str = "dev-key-change-me"
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"
    pymupdf_min_char_threshold: int = 100
    extraction_version: str = "v1"
    capability_taxonomy_version: str = "v1"
    resume_storage_backend: Literal["local", "supabase"] = "local"
    resume_storage_path: str = "./data/resumes"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_storage_bucket: str = "resumes"
    log_level: str = "INFO"
    cors_origins: str = ""
    resend_api_key: str = ""
    email_from: str = "Job Scout <notifications@job-scout.dev>"
    gcp_project: str = ""
    embedding_requests_topic: str = "embedding-requests"
    embedding_publish_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def resume_storage_dir(self) -> Path:
        return Path(self.resume_storage_path)

    @property
    def should_publish_embedding_requests(self) -> bool:
        return self.embedding_publish_enabled and bool(self.gcp_project.strip())

    @property
    def allowed_cors_origins(self) -> list[str]:
        defaults = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
            "https://job-scout.dev",
            "https://carrier-match-gcp.vercel.app",
        ]
        if not self.cors_origins.strip():
            return defaults
        extra = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return list(dict.fromkeys(defaults + extra))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
