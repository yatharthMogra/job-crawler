from __future__ import annotations

import structlog
from pathlib import Path
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.h1b.aggregate import aggregate_lca_stats, aggregate_uscis_stats
from app.ingestion.h1b.load_lca import load_lca_file
from app.ingestion.h1b.load_uscis import load_uscis_file
from app.ingestion.h1b.matching import build_company_lookup, match_employer, upsert_employer_alias
from app.ingestion.h1b.normalize import normalize_employer_name
from app.ingestion.h1b.rebuild_summary import rebuild_company_pool_summary
from app.models.h1b import H1bEmployer, LcaRaw, UscisRaw

log = structlog.get_logger(__name__)

_REVIEW_LCA_THRESHOLD = 50


async def normalize_all_employers(db: AsyncSession, *, dry_run: bool = False) -> dict[str, int | float]:
    lca_names = await db.scalars(select(LcaRaw.employer_name_raw).distinct())
    uscis_names = await db.scalars(select(UscisRaw.employer_name_raw).distinct())
    raw_names = set(lca_names.all()) | set(uscis_names.all())

    company_lookup = await build_company_lookup(db)
    stats = {
        "total_raw": len(raw_names),
        "exact": 0,
        "fuzzy_auto": 0,
        "fuzzy_candidate": 0,
        "unmatched": 0,
        "manual": 0,
    }

    for raw_name in raw_names:
        match = await match_employer(db, raw_name, company_lookup=company_lookup)
        stats[match.match_method] = stats.get(match.match_method, 0) + 1
        if dry_run:
            continue
        norm_name = normalize_employer_name(raw_name)
        await upsert_employer_alias(
            db,
            raw_name=raw_name,
            norm_name=norm_name,
            first_seen_year=None,
            match=match,
        )

    if not dry_run:
        await db.commit()

    matched = stats["exact"] + stats["fuzzy_auto"] + stats.get("manual", 0)
    stats["match_rate_pct"] = round(100.0 * matched / stats["total_raw"], 1) if stats["total_raw"] else 0.0
    log.info("h1b_employer_normalization_complete", **stats)
    return stats


async def run_h1b_ingestion(
    db: AsyncSession,
    *,
    lca_path: Path | None = None,
    uscis_path: Path | None = None,
    uscis_fiscal_year: int | None = None,
    skip_load: bool = False,
) -> dict[str, object]:
    results: dict[str, object] = {}

    if not skip_load:
        if lca_path:
            results["lca_load"] = await load_lca_file(db, lca_path)
        if uscis_path:
            results["uscis_load"] = await load_uscis_file(
                db, uscis_path, default_fiscal_year=uscis_fiscal_year
            )

    results["normalization"] = await normalize_all_employers(db)
    results["lca_stats_rows"] = await aggregate_lca_stats(db)
    results["uscis_stats_rows"] = await aggregate_uscis_stats(db)
    results["summary_rows"] = await rebuild_company_pool_summary(db)

    norm_stats = results["normalization"]
    if isinstance(norm_stats, dict):
        high_volume_unmatched = await _high_volume_unmatched_rate(db)
        results["high_volume_match_rate_pct"] = high_volume_unmatched
        if high_volume_unmatched < 80.0:
            log.warning(
                "h1b_high_volume_match_rate_low",
                rate=high_volume_unmatched,
                threshold=80.0,
            )

    return results


async def _high_volume_unmatched_rate(db: AsyncSession) -> float:
    """Match rate for employers with >50 certified LCAs in any year."""
    high_volume = await db.execute(
        select(LcaRaw.employer_name_raw, func.count())
        .where(LcaRaw.case_status.ilike("certified"))
        .group_by(LcaRaw.employer_name_raw)
        .having(func.count() > _REVIEW_LCA_THRESHOLD)
    )
    high_volume_norms: set[str] = set()
    for raw_name, _ in high_volume.all():
        norm = normalize_employer_name(raw_name)
        if norm:
            high_volume_norms.add(norm)

    if not high_volume_norms:
        return 100.0

    matched = await db.scalars(
        select(H1bEmployer.employer_name_norm).where(
            H1bEmployer.employer_name_norm.in_(high_volume_norms),
            H1bEmployer.company_id.isnot(None),
        )
    )
    matched_count = len(set(matched.all()))
    return round(100.0 * matched_count / len(high_volume_norms), 1)
