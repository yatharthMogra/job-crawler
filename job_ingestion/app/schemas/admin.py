from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

NO_POOL_THRESHOLD_PCT = 10.0
TOP_TITLES_LIMIT = 10


class NoPoolTitleOut(BaseModel):
    title: str
    count: int


class DomainTaxonomyHealthOut(BaseModel):
    domain: str
    total: int
    no_pool: int
    no_pool_pct: float
    flagged: bool
    top_no_pool_titles: list[NoPoolTitleOut]


class TaxonomyHealthOut(BaseModel):
    generated_at: datetime
    total_active_enriched: int
    global_no_pool_count: int
    global_no_pool_pct: float
    domains: list[DomainTaxonomyHealthOut]
