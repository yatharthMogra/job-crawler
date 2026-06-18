from __future__ import annotations

import uuid

from app.services.h1b_lookup import H1bLookup, H1bSummaryRow


def compute_sponsorship_score(
    company_id: uuid.UUID,
    pool_family: str | None,
    candidate_needs_sponsorship: bool,
    summary_lookup: H1bLookup | None,
) -> float:
    """Returns 0.0–1.0 bonus weight."""
    if not candidate_needs_sponsorship:
        return 0.5

    if pool_family is None:
        return 0.1

    key = (company_id, pool_family)
    if not summary_lookup or key not in summary_lookup:
        return 0.1

    row = summary_lookup[key]
    if row.is_top_sponsor:
        return 1.0
    if row.total_lca_3yr >= 20:
        return 0.8
    if row.total_lca_3yr >= 5:
        return 0.5
    return 0.2


def h1b_info_from_lookup(
    company_id: uuid.UUID,
    pool_family: str | None,
    summary_lookup: H1bLookup | None,
) -> H1bSummaryRow | None:
    if pool_family is None or not summary_lookup:
        return None
    return summary_lookup.get((company_id, pool_family))
