import uuid
from unittest.mock import MagicMock, patch

import pytest

from app.config import Settings
from app.exceptions import ExtractionError
from app.storage.azure_blob import AzureBlobResumeStorage
from app.storage.base import resume_storage_key
from app.storage.factory import get_resume_storage
from app.storage.local import LocalResumeStorage


def test_resume_storage_key_format() -> None:
    candidate_id = uuid.UUID("00000000-0000-4000-8000-000000000001")
    resume_id = uuid.UUID("00000000-0000-4000-8000-000000000002")
    assert resume_storage_key(candidate_id, resume_id) == (
        "00000000-0000-4000-8000-000000000001/00000000-0000-4000-8000-000000000002.pdf"
    )


def test_local_resume_storage_round_trip(tmp_path) -> None:
    settings = Settings(resume_storage_path=str(tmp_path))
    storage = LocalResumeStorage(settings)
    candidate_id = uuid.uuid4()
    resume_id = uuid.uuid4()
    content = b"%PDF-1.4 test content"

    key = storage.save(candidate_id, resume_id, content)
    assert key == resume_storage_key(candidate_id, resume_id)
    assert storage.read_bytes(key) == content


def test_factory_selects_azure_backend() -> None:
    settings = Settings(
        resume_storage_backend="azure",
        azure_storage_connection_string="UseDevelopmentStorage=true",
    )
    with patch("app.storage.azure_blob.BlobServiceClient") as mock_client_cls:
        mock_client_cls.from_connection_string.return_value = MagicMock()
        storage = get_resume_storage(settings)
    assert isinstance(storage, AzureBlobResumeStorage)


def test_azure_blob_storage_round_trip() -> None:
    settings = Settings(
        resume_storage_backend="azure",
        azure_storage_connection_string="UseDevelopmentStorage=true",
        azure_storage_container="resumes",
    )
    candidate_id = uuid.uuid4()
    resume_id = uuid.uuid4()
    content = b"%PDF-1.4 azure content"
    key = resume_storage_key(candidate_id, resume_id)

    blob_client = MagicMock()
    downloader = MagicMock()
    downloader.readall.return_value = content
    blob_client.download_blob.return_value = downloader

    container_client = MagicMock()
    container_client.get_blob_client.return_value = blob_client

    service_client = MagicMock()
    service_client.get_container_client.return_value = container_client

    with patch(
        "app.storage.azure_blob.BlobServiceClient.from_connection_string",
        return_value=service_client,
    ):
        storage = AzureBlobResumeStorage(settings)
        assert storage.save(candidate_id, resume_id, content) == key
        assert storage.read_bytes(key) == content

    blob_client.upload_blob.assert_called_once()
    upload_kwargs = blob_client.upload_blob.call_args
    assert upload_kwargs.args[0] == content
    assert upload_kwargs.kwargs["overwrite"] is True
    container_client.get_blob_client.assert_called_with(key)


def test_azure_blob_storage_requires_connection_string() -> None:
    settings = Settings(resume_storage_backend="azure", azure_storage_connection_string="")
    with pytest.raises(ValueError, match="AZURE_STORAGE_CONNECTION_STRING"):
        AzureBlobResumeStorage(settings)


def test_azure_blob_download_missing_raises() -> None:
    from azure.core.exceptions import ResourceNotFoundError

    settings = Settings(
        azure_storage_connection_string="UseDevelopmentStorage=true",
        azure_storage_container="resumes",
    )
    blob_client = MagicMock()
    blob_client.download_blob.side_effect = ResourceNotFoundError("missing")

    container_client = MagicMock()
    container_client.get_blob_client.return_value = blob_client

    service_client = MagicMock()
    service_client.get_container_client.return_value = container_client

    with patch(
        "app.storage.azure_blob.BlobServiceClient.from_connection_string",
        return_value=service_client,
    ):
        storage = AzureBlobResumeStorage(settings)
        with pytest.raises(ExtractionError, match="not found"):
            storage.read_bytes("missing/key.pdf")
