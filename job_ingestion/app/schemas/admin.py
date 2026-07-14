from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel

NO_POOL_THRESHOLD_PCT = 10.0
TOP_TITLES_LIMIT = 10


class NoPoolTitleOut(BaseModel):
    title: str
    count: int


class DomainTaxonomyHealthOut(BaseModel):
    """One taxonomy group row. `domain` holds the group key (domain or role name)."""

    domain: str
    total: int
    no_pool: int
    no_pool_pct: float
    flagged: bool
    acknowledged: bool = False
    acknowledged_at: datetime | None = None
    needs_review: bool = False
    top_no_pool_titles: list[NoPoolTitleOut]


class TaxonomyHealthOut(BaseModel):
    generated_at: datetime
    group_by: str = "domain"
    total_active_enriched: int
    global_no_pool_count: int
    global_no_pool_pct: float
    domains_flagged: int
    domains_needing_review: int
    domains: list[DomainTaxonomyHealthOut]


class TaxonomyHealthAckIn(BaseModel):
    acknowledged: bool


class H1bLcaYearOut(BaseModel):
    fiscal_year: int
    count: int


class H1bStatsOut(BaseModel):
    generated_at: datetime
    total_employers: int
    matched_employers: int
    unmatched_employers: int
    match_rate_pct: float
    lca_rows_by_year: list[H1bLcaYearOut]
    total_lca_rows: int


class H1bReviewQueueItemOut(BaseModel):
    id: int
    employer_name_norm: str
    match_method: str
    match_confidence: float | None
    total_lca: int


class H1bReviewQueueOut(BaseModel):
    items: list[H1bReviewQueueItemOut]


class H1bCoverageItemOut(BaseModel):
    pool_family: str
    tracked_companies: int
    companies_with_data: int
    coverage_pct: float
    flagged: bool


class H1bCoverageOut(BaseModel):
    items: list[H1bCoverageItemOut]


class H1bEmployerLinkIn(BaseModel):
    company_id: uuid.UUID


class H1bEmployerOut(BaseModel):
    id: int
    employer_name_norm: str
    company_id: uuid.UUID | None
    match_method: str | None
    match_confidence: float | None

    model_config = {"from_attributes": True}


class H1bIngestResultOut(BaseModel):
    status: str
    results: dict[str, object]
