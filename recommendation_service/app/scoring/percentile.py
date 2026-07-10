from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PoolCutoffs:
    p50: float
    p75: float
    p90: float
    p95: float


def _parse_cutoffs(raw: dict[str, Any] | None) -> PoolCutoffs | None:
    if not raw:
        return None
    try:
        return PoolCutoffs(
            p50=float(raw["p50"]),
            p75=float(raw["p75"]),
            p90=float(raw["p90"]),
            p95=float(raw["p95"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def percentile_from_score(score: float, cutoffs: PoolCutoffs) -> tuple[int, str]:
    normalized = max(0.0, min(1.0, score))
    if normalized >= cutoffs.p95:
        return 95, "Top 5%"
    if normalized >= cutoffs.p90:
        return 90, "Top 10%"
    if normalized >= cutoffs.p75:
        pct = 75 + int(((normalized - cutoffs.p75) / max(cutoffs.p90 - cutoffs.p75, 1e-6)) * 14)
        return min(89, pct), f"{pct}th percentile"
    if normalized >= cutoffs.p50:
        pct = 50 + int(((normalized - cutoffs.p50) / max(cutoffs.p75 - cutoffs.p50, 1e-6)) * 24)
        return min(74, pct), f"{pct}th percentile"
    pct = max(1, int((normalized / max(cutoffs.p50, 1e-6)) * 49))
    return pct, f"{pct}th percentile"


def pick_pool_for_percentile(
    job_pools: list[str],
    user_pools: list[str],
) -> str | None:
    overlap = [pool for pool in job_pools if pool in user_pools]
    return overlap[0] if overlap else (job_pools[0] if job_pools else None)


def resolve_pool_percentile(
    *,
    semantic_score: float | None,
    pool_percentile_cutoffs: dict[str, Any] | None,
    job_pools: list[str],
    user_pools: list[str],
) -> tuple[int | None, str | None]:
    if semantic_score is None or not pool_percentile_cutoffs:
        return None, None
    pool = pick_pool_for_percentile(job_pools, user_pools)
    if pool is None:
        return None, None
    cutoffs = _parse_cutoffs(pool_percentile_cutoffs.get(pool))
    if cutoffs is None:
        return None, None
    return percentile_from_score(semantic_score, cutoffs)
