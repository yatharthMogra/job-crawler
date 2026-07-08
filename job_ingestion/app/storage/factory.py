from __future__ import annotations

from functools import lru_cache

from app.config import Settings, get_settings
from app.storage.base import CompanyLogoStorage
from app.storage.local import LocalCompanyLogoStorage
from app.storage.supabase import SupabaseCompanyLogoStorage


@lru_cache(maxsize=1)
def get_company_logo_storage(settings: Settings | None = None) -> CompanyLogoStorage:
    resolved = settings or get_settings()
    if resolved.company_logo_storage_backend == "supabase":
        return SupabaseCompanyLogoStorage(resolved)
    return LocalCompanyLogoStorage(resolved)
