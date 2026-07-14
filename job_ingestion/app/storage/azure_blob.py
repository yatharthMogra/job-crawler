from __future__ import annotations

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, ContentSettings

from app.config import Settings
from app.storage.base import company_logo_storage_key


class AzureBlobCompanyLogoStorage:
    """Upload company logos to Azure Blob; public_url must be browser-reachable."""

    def __init__(self, settings: Settings) -> None:
        if not settings.azure_storage_connection_string.strip():
            raise ValueError("Azure logo storage requires AZURE_STORAGE_CONNECTION_STRING")
        public_base = settings.company_logo_public_base_url.strip().rstrip("/")
        if not public_base.startswith(("http://", "https://")):
            raise ValueError(
                "Azure logo storage requires COMPANY_LOGO_PUBLIC_BASE_URL "
                "to be an absolute https URL (e.g. "
                "https://<account>.blob.core.windows.net/<container>)"
            )
        self._public_base = public_base
        self._container = settings.azure_storage_container.strip() or "company-logos"
        self._client = BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
        self._container_client = self._client.get_container_client(self._container)

    def save(self, board_token: str, content: bytes) -> str:
        key = company_logo_storage_key(board_token)
        blob = self._container_client.get_blob_client(key)
        try:
            blob.upload_blob(
                content,
                overwrite=True,
                content_settings=ContentSettings(content_type="image/png"),
            )
        except AzureError as exc:
            raise RuntimeError(f"Azure logo upload failed: {exc}") from exc
        return self.public_url(board_token)

    def public_url(self, board_token: str) -> str:
        key = company_logo_storage_key(board_token)
        return f"{self._public_base}/{key}"
