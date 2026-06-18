from datetime import datetime
from typing import Any

from app.exceptions import UnsupportedPlatformError
from app.ingestion.connectors.ashby import AshbyConnector
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.connectors.greenhouse import GreenhouseConnector
from app.ingestion.connectors.lever import LeverConnector
from app.ingestion.connectors.icims import ICIMSConnector
from app.ingestion.connectors.oracle_hcm import OracleHCMConnector
from app.ingestion.connectors.workable import WorkableConnector
from app.ingestion.connectors.workatastartup import WorkAtAStartupConnector
from app.ingestion.connectors.workday import WorkdayConnector
from app.models.company import Company


CONNECTORS: dict[str, type[BaseConnector]] = {
    "greenhouse": GreenhouseConnector,
    "lever": LeverConnector,
    "ashby": AshbyConnector,
    "workday": WorkdayConnector,
    "oracle_hcm": OracleHCMConnector,
    "icims": ICIMSConnector,
    "workable": WorkableConnector,
    "workatastartup": WorkAtAStartupConnector,
}


def get_connector(platform: str) -> BaseConnector:
    connector_cls = CONNECTORS.get(platform.lower())
    if connector_cls is None:
        raise UnsupportedPlatformError(f"Unsupported platform: {platform}")
    return connector_cls()


async def fetch_company_jobs(
    company: Company,
    *,
    known_raw_by_id: dict[str, dict[str, Any]] | None = None,
    known_raw_fetched_at: dict[str, datetime] | None = None,
) -> list[dict[str, Any]]:
    connector = get_connector(company.platform)
    if company.platform == "workday":
        return await connector.fetch_jobs(
            company,
            known_raw_by_id=known_raw_by_id or {},
            known_raw_fetched_at=known_raw_fetched_at or {},
        )
    return await connector.fetch_jobs(company)
