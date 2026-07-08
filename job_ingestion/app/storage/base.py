from __future__ import annotations

from typing import Protocol


def company_logo_storage_key(board_token: str) -> str:
    safe = board_token.strip().lower().replace("/", "-")
    return f"{safe}.png"


class CompanyLogoStorage(Protocol):
    def save(self, board_token: str, content: bytes) -> str:
        """Persist logo bytes and return the public URL."""

    def public_url(self, board_token: str) -> str:
        """Return the public URL for a stored logo."""
