from __future__ import annotations

from app.config import Settings
from app.storage.base import ResumeStorage
from app.storage.local import LocalResumeStorage
from app.storage.supabase import SupabaseResumeStorage


def get_resume_storage(settings: Settings) -> ResumeStorage:
    if settings.resume_storage_backend == "supabase":
        return SupabaseResumeStorage(settings)
    return LocalResumeStorage(settings)
