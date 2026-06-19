from __future__ import annotations

import uuid
from pathlib import Path

from app.config import Settings
from app.storage.base import ResumeStorage, resume_storage_key


class LocalResumeStorage:
    def __init__(self, settings: Settings) -> None:
        self._root = settings.resume_storage_dir

    def save(self, candidate_id: uuid.UUID, resume_id: uuid.UUID, content: bytes) -> str:
        key = resume_storage_key(candidate_id, resume_id)
        path = self._root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return key

    def read_bytes(self, key: str) -> bytes:
        path = self._root / key
        return Path(path).read_bytes()
