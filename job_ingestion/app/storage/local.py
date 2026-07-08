from __future__ import annotations

from pathlib import Path

from app.config import Settings
from app.storage.base import CompanyLogoStorage, company_logo_storage_key


class LocalCompanyLogoStorage:
    def __init__(self, settings: Settings) -> None:
        self._root = settings.company_logo_dir
        self._public_base = settings.company_logo_public_base_url.rstrip("/")

    def save(self, board_token: str, content: bytes) -> str:
        key = company_logo_storage_key(board_token)
        path = self._root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return self.public_url(board_token)

    def public_url(self, board_token: str) -> str:
        key = company_logo_storage_key(board_token)
        return f"{self._public_base}/{key}"

    def read_bytes(self, board_token: str) -> bytes:
        path = self._root / company_logo_storage_key(board_token)
        return Path(path).read_bytes()
