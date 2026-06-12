from typing import Any

from app.exceptions import UnsupportedPlatformError
from app.ingestion.connectors.ashby import AshbyConnector
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.connectors.greenhouse import GreenhouseConnector
from app.ingestion.connectors.lever import LeverConnector
from app.ingestion.connectors.oracle_hcm import OracleHCMConnector
from app.ingestion.connectors.workday import WorkdayConnector
from app.models.company import Company


CONNECTORS: dict[str, type[BaseConnector]] = {
    "greenhouse": GreenhouseConnector,
    "lever": LeverConnector,
    "ashby": AshbyConnector,
    "workday": WorkdayConnector,
    "oracle_hcm": OracleHCMConnector,
}


def get_connector(platform: str) -> BaseConnector:
    connector_cls = CONNECTORS.get(platform.lower())
    if connector_cls is None:
        raise UnsupportedPlatformError(f"Unsupported platform: {platform}")
    return connector_cls()


async def fetch_company_jobs(company: Company) -> list[dict[str, Any]]:
    connector = get_connector(company.platform)
    return await connector.fetch_jobs(company)
