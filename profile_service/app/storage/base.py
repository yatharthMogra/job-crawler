from __future__ import annotations

import uuid
from typing import Protocol


def resume_storage_key(candidate_id: uuid.UUID, resume_id: uuid.UUID) -> str:
    return f"{candidate_id}/{resume_id}.pdf"


class ResumeStorage(Protocol):
    def save(self, candidate_id: uuid.UUID, resume_id: uuid.UUID, content: bytes) -> str:
        """Persist PDF bytes and return the storage key."""

    def read_bytes(self, key: str) -> bytes:
        """Load PDF bytes for the given storage key."""
