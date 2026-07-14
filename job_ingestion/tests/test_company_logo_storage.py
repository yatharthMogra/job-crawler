from unittest.mock import MagicMock, patch

import pytest

from app.config import Settings
from app.storage.azure_blob import AzureBlobCompanyLogoStorage
from app.storage.base import company_logo_storage_key
from app.storage.factory import get_company_logo_storage
from app.storage.local import LocalCompanyLogoStorage


def test_company_logo_storage_key() -> None:
    assert company_logo_storage_key("Acme/Corp") == "acme-corp.png"


def test_local_company_logo_round_trip(tmp_path) -> None:
    settings = Settings(
        company_logo_storage_backend="local",
        company_logo_local_dir=str(tmp_path),
        company_logo_public_base_url="/logos/companies",
    )
    storage = LocalCompanyLogoStorage(settings)
    content = b"\x89PNG\r\n\x1a\nfake"
    url = storage.save("acme", content)
    assert url == "/logos/companies/acme.png"
    assert storage.read_bytes("acme") == content


def test_factory_selects_azure_logo_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = Settings(
        company_logo_storage_backend="azure",
        azure_storage_connection_string="UseDevelopmentStorage=true",
        azure_storage_container="company-icons",
        company_logo_public_base_url="https://acct.blob.core.windows.net/company-logos",
    )
    get_company_logo_storage.cache_clear()
    monkeypatch.setattr("app.storage.factory.get_settings", lambda: settings)
    with patch("app.storage.azure_blob.BlobServiceClient") as mock_cls:
        mock_cls.from_connection_string.return_value = MagicMock()
        storage = get_company_logo_storage()
    assert isinstance(storage, AzureBlobCompanyLogoStorage)
    get_company_logo_storage.cache_clear()


def test_azure_logo_save_returns_public_url() -> None:
    settings = Settings(
        company_logo_storage_backend="azure",
        azure_storage_connection_string="UseDevelopmentStorage=true",
        azure_storage_container="company-logos",
        company_logo_public_base_url="https://acct.blob.core.windows.net/company-logos",
    )
    blob_client = MagicMock()
    container_client = MagicMock()
    container_client.get_blob_client.return_value = blob_client
    service_client = MagicMock()
    service_client.get_container_client.return_value = container_client

    with patch(
        "app.storage.azure_blob.BlobServiceClient.from_connection_string",
        return_value=service_client,
    ):
        storage = AzureBlobCompanyLogoStorage(settings)
        url = storage.save("stripe", b"\x89PNG")

    assert url == "https://acct.blob.core.windows.net/company-logos/stripe.png"
    blob_client.upload_blob.assert_called_once()
    assert blob_client.upload_blob.call_args.kwargs["overwrite"] is True


def test_azure_logo_requires_public_https_base() -> None:
    settings = Settings(
        azure_storage_connection_string="UseDevelopmentStorage=true",
        company_logo_public_base_url="/logos/companies",
    )
    with pytest.raises(ValueError, match="COMPANY_LOGO_PUBLIC_BASE_URL"):
        AzureBlobCompanyLogoStorage(settings)


def test_azure_logo_requires_connection_string() -> None:
    settings = Settings(
        azure_storage_connection_string="",
        company_logo_public_base_url="https://acct.blob.core.windows.net/company-logos",
    )
    with pytest.raises(ValueError, match="AZURE_STORAGE_CONNECTION_STRING"):
        AzureBlobCompanyLogoStorage(settings)
