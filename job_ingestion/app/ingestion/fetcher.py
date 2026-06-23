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
from app.ingestion.connectors.bamboohr import BambooHRConnector
from app.ingestion.connectors.rippling import RipplingConnector
from app.ingestion.connectors.smartrecruiters import SmartRecruitersConnector
from app.ingestion.connectors.google_careers import GoogleCareersConnector
from app.ingestion.connectors.amazon_jobs import AmazonJobsConnector
from app.ingestion.connectors.tesla_careers import TeslaCareersConnector, is_manual_push_company
from app.ingestion.connectors.successfactors import SuccessFactorsConnector
from app.ingestion.connectors.workday import WorkdayConnector
from app.ingestion.connectors.talentbrew import TalentBrewConnector
from app.ingestion.connectors.apple_careers import AppleCareersConnector
from app.ingestion.connectors.eightfold import EightfoldConnector
from app.ingestion.job_freshness import filter_fetched_jobs
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
    "smartrecruiters": SmartRecruitersConnector,
    "bamboohr": BambooHRConnector,
    "rippling": RipplingConnector,
    "successfactors": SuccessFactorsConnector,
    "google_careers": GoogleCareersConnector,
    "amazon_jobs": AmazonJobsConnector,
    "tesla_careers": TeslaCareersConnector,
    "talentbrew": TalentBrewConnector,
    "apple_careers": AppleCareersConnector,
    "eightfold": EightfoldConnector,
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
) -> tuple[list[dict[str, Any]], int]:
    if is_manual_push_company(company):
        from app.exceptions import ConnectorFetchError

        raise ConnectorFetchError(
            f"{company.name} uses manual_push ingestion; use the browser bridge instead",
            None,
        )
    connector = get_connector(company.platform)
    if company.platform in ("workday", "ashby"):
        jobs = await connector.fetch_jobs(
            company,
            known_raw_by_id=known_raw_by_id or {},
            known_raw_fetched_at=known_raw_fetched_at or {},
        )
    else:
        jobs = await connector.fetch_jobs(company)
    filtered, rejected = filter_fetched_jobs(jobs, company.platform)
    return filtered, rejected
