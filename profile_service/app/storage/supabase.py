from __future__ import annotations

import uuid

import httpx

from app.config import Settings
from app.exceptions import ExtractionError
from app.storage.base import ResumeStorage, resume_storage_key


class SupabaseResumeStorage:
    def __init__(self, settings: Settings) -> None:
        if not settings.supabase_url or not settings.supabase_service_role_key:
            raise ValueError("Supabase storage requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
        self._base_url = settings.supabase_url.rstrip("/")
        self._api_key = settings.supabase_service_role_key
        self._bucket = settings.supabase_storage_bucket

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "apikey": self._api_key,
        }

    def save(self, candidate_id: uuid.UUID, resume_id: uuid.UUID, content: bytes) -> str:
        key = resume_storage_key(candidate_id, resume_id)
        url = f"{self._base_url}/storage/v1/object/{self._bucket}/{key}"
        response = httpx.post(
            url,
            headers={**self._headers(), "Content-Type": "application/pdf", "x-upsert": "true"},
            content=content,
            timeout=60.0,
        )
        if response.status_code not in (200, 201):
            raise ExtractionError(f"Supabase upload failed ({response.status_code}): {response.text}")
        return key

    def read_bytes(self, key: str) -> bytes:
        url = f"{self._base_url}/storage/v1/object/{self._bucket}/{key}"
        response = httpx.get(url, headers=self._headers(), timeout=60.0)
        if response.status_code != 200:
            raise ExtractionError(f"Supabase download failed ({response.status_code}): {response.text}")
        return response.content
