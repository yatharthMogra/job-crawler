from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.models.company import Company
from app.models.enrichment_queue import EnrichmentQueue

if TYPE_CHECKING:
    from app.config import FetchBackpressureMode

logger = logging.getLogger(__name__)

WORKATASTARTUP_PLATFORM = "workatastartup"
PENDING_STATUSES = ("queued", "cooldown", "in_progress")


@dataclass(frozen=True)
class BackpressureDecision:
    enabled: bool
    active: bool
    depth: int
    threshold: int
    mode: FetchBackpressureMode
    skip_tiers: frozenset[int]
    allow_waas: bool
    companies_before: int = 0
    companies_after: int = 0

    def with_company_counts(self, *, before: int, after: int) -> BackpressureDecision:
        return BackpressureDecision(
            enabled=self.enabled,
            active=self.active,
            depth=self.depth,
            threshold=self.threshold,
            mode=self.mode,
            skip_tiers=self.skip_tiers,
            allow_waas=self.allow_waas,
            companies_before=before,
            companies_after=after,
        )


async def get_pending_queue_depth(db: AsyncSession) -> int:
    depth = await db.scalar(
        select(func.count())
        .select_from(EnrichmentQueue)
        .where(EnrichmentQueue.status.in_(PENDING_STATUSES))
    )
    return int(depth or 0)


def evaluate_backpressure(
    depth: int,
    settings: Optional[Settings] = None,
) -> BackpressureDecision:
    settings = settings or get_settings()
    threshold = settings.fetch_backpressure_queue_threshold
    enabled = settings.fetch_backpressure_enabled
    active = enabled and depth >= threshold
    return BackpressureDecision(
        enabled=enabled,
        active=active,
        depth=depth,
        threshold=threshold,
        mode=settings.fetch_backpressure_mode,
        skip_tiers=frozenset(settings.fetch_backpressure_skip_tiers_set()),
        allow_waas=settings.fetch_backpressure_allow_waas,
    )


def apply_backpressure_to_companies(
    companies: list[Company],
    decision: BackpressureDecision,
) -> list[Company]:
    if not decision.active:
        return companies

    if decision.mode == "halt_all":
        if decision.allow_waas:
            return [company for company in companies if company.platform == WORKATASTARTUP_PLATFORM]
        return []

    skip_tiers = decision.skip_tiers
    return [company for company in companies if company.fetch_tier not in skip_tiers]


def backpressure_metadata(decision: BackpressureDecision) -> dict:
    return {
        "enabled": decision.enabled,
        "active": decision.active,
        "depth": decision.depth,
        "threshold": decision.threshold,
        "mode": decision.mode,
        "skip_tiers": sorted(decision.skip_tiers),
        "allow_waas": decision.allow_waas,
        "companies_before": decision.companies_before,
        "companies_after": decision.companies_after,
    }


async def apply_fetch_backpressure(
    db: AsyncSession,
    companies: list[Company],
    *,
    settings: Optional[Settings] = None,
) -> tuple[list[Company], BackpressureDecision]:
    settings = settings or get_settings()
    if not settings.fetch_backpressure_enabled:
        decision = evaluate_backpressure(0, settings=settings).with_company_counts(
            before=len(companies),
            after=len(companies),
        )
        return companies, decision

    depth = await get_pending_queue_depth(db)
    decision = evaluate_backpressure(depth, settings=settings)
    filtered = apply_backpressure_to_companies(companies, decision)
    decision = decision.with_company_counts(before=len(companies), after=len(filtered))
    if decision.active:
        logger.info(
            "fetch_backpressure_active depth=%s threshold=%s mode=%s companies_before=%s companies_after=%s",
            decision.depth,
            decision.threshold,
            decision.mode,
            decision.companies_before,
            decision.companies_after,
        )
    return filtered, decision
