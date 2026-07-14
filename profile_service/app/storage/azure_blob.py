from __future__ import annotations

import uuid

from azure.core.exceptions import AzureError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, ContentSettings

from app.config import Settings
from app.exceptions import ExtractionError
from app.storage.base import resume_storage_key


class AzureBlobResumeStorage:
    def __init__(self, settings: Settings) -> None:
        if not settings.azure_storage_connection_string.strip():
            raise ValueError("Azure storage requires AZURE_STORAGE_CONNECTION_STRING")
        self._container = settings.azure_storage_container.strip() or "resumes"
        self._client = BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
        self._container_client = self._client.get_container_client(self._container)

    def save(self, candidate_id: uuid.UUID, resume_id: uuid.UUID, content: bytes) -> str:
        key = resume_storage_key(candidate_id, resume_id)
        blob = self._container_client.get_blob_client(key)
        try:
            blob.upload_blob(
                content,
                overwrite=True,
                content_settings=ContentSettings(content_type="application/pdf"),
            )
        except AzureError as exc:
            raise ExtractionError(f"Azure blob upload failed: {exc}") from exc
        return key

    def read_bytes(self, key: str) -> bytes:
        blob = self._container_client.get_blob_client(key)
        try:
            return blob.download_blob().readall()
        except ResourceNotFoundError as exc:
            raise ExtractionError(f"Azure blob not found: {key}") from exc
        except AzureError as exc:
            raise ExtractionError(f"Azure blob download failed: {exc}") from exc
