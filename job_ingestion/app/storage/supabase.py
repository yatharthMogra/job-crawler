from __future__ import annotations

import httpx

from app.config import Settings
from app.storage.base import CompanyLogoStorage, company_logo_storage_key


class SupabaseCompanyLogoStorage:
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

    def save(self, board_token: str, content: bytes) -> str:
        key = f"company-logos/{company_logo_storage_key(board_token)}"
        url = f"{self._base_url}/storage/v1/object/{self._bucket}/{key}"
        response = httpx.post(
            url,
            headers={**self._headers(), "Content-Type": "image/png", "x-upsert": "true"},
            content=content,
            timeout=60.0,
        )
        if response.status_code not in (200, 201):
            raise RuntimeError(f"Supabase logo upload failed ({response.status_code}): {response.text}")
        return self.public_url(board_token)

    def public_url(self, board_token: str) -> str:
        key = f"company-logos/{company_logo_storage_key(board_token)}"
        return f"{self._base_url}/storage/v1/object/public/{self._bucket}/{key}"
