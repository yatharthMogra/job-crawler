from __future__ import annotations

from collections import Counter
from decimal import Decimal

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.h1b.normalize import normalize_employer_name
from app.ingestion.h1b.wages import normalize_wage_to_annual
from app.models.h1b import H1bEmployer, H1bLcaStats, H1bUscisStats, LcaRaw, SocToPoolMapping, UscisRaw


async def aggregate_lca_stats(db: AsyncSession) -> int:
    """Rebuild h1b_lca_stats from lca_raw joined with employer aliases."""
    await db.execute(delete(H1bLcaStats))

    soc_map = {
        row.soc_code: row.pool_family
        for row in (await db.scalars(select(SocToPoolMapping))).all()
    }

    rows = await db.execute(
        select(
            LcaRaw.employer_name_raw,
            LcaRaw.soc_code,
            LcaRaw.fiscal_year,
            LcaRaw.case_status,
            LcaRaw.wage_from,
            LcaRaw.wage_unit,
            LcaRaw.worksite_state,
        )
    )

    buckets: dict[tuple[str, str | None, int], dict] = {}

    for raw_name, soc_code, fy, status, wage_from, wage_unit, state in rows.all():
        norm = normalize_employer_name(raw_name)
        if not norm:
            continue
        key = (norm, soc_code, fy)
        bucket = buckets.setdefault(
            key,
            {
                "certified": 0,
                "denied": 0,
                "withdrawn": 0,
                "wages": [],
                "states": [],
            },
        )
        status_norm = (status or "").strip().lower()
        if status_norm == "certified":
            bucket["certified"] += 1
        elif status_norm == "denied":
            bucket["denied"] += 1
        elif status_norm == "withdrawn":
            bucket["withdrawn"] += 1
        annual = normalize_wage_to_annual(wage_from, wage_unit)
        if annual:
            bucket["wages"].append(annual)
        if state:
            bucket["states"].append(state)

    employers = {
        e.employer_name_norm: e.company_id
        for e in (await db.scalars(select(H1bEmployer))).all()
    }

    count = 0
    for (norm, soc_code, fy), data in buckets.items():
        state_counts = Counter(data["states"])
        primary_state = state_counts.most_common(1)[0][0] if state_counts else None
        avg_wage = (
            Decimal(str(sum(data["wages"]) / len(data["wages"])))
            if data["wages"]
            else None
        )
        db.add(
            H1bLcaStats(
                employer_name_norm=norm,
                company_id=employers.get(norm),
                soc_code=soc_code,
                pool_family=soc_map.get(soc_code or ""),
                fiscal_year=fy,
                lca_certified=data["certified"],
                lca_denied=data["denied"],
                lca_withdrawn=data["withdrawn"],
                avg_wage_annual=avg_wage,
                primary_state=primary_state,
            )
        )
        count += 1

    await db.commit()
    return count


async def aggregate_uscis_stats(db: AsyncSession) -> int:
    """Rebuild h1b_uscis_stats from uscis_raw."""
    await db.execute(delete(H1bUscisStats))

    rows = await db.execute(
        select(
            UscisRaw.employer_name_raw,
            UscisRaw.fiscal_year,
            func.sum(UscisRaw.initial_approvals),
            func.sum(UscisRaw.initial_denials),
            func.sum(UscisRaw.continuing_approvals),
            func.sum(UscisRaw.continuing_denials),
        ).group_by(UscisRaw.employer_name_raw, UscisRaw.fiscal_year)
    )

    employers = {
        e.employer_name_norm: e.company_id
        for e in (await db.scalars(select(H1bEmployer))).all()
    }

    count = 0
    for raw_name, fy, init_app, init_den, cont_app, cont_den in rows.all():
        norm = normalize_employer_name(raw_name)
        if not norm:
            continue
        init_app = int(init_app or 0)
        init_den = int(init_den or 0)
        total = init_app + init_den
        approval_rate = Decimal(str(round(init_app / total, 4))) if total > 0 else None
        db.add(
            H1bUscisStats(
                employer_name_norm=norm,
                company_id=employers.get(norm),
                fiscal_year=fy,
                initial_approvals=init_app,
                initial_denials=init_den,
                continuing_approvals=int(cont_app or 0),
                continuing_denials=int(cont_den or 0),
                approval_rate=approval_rate,
            )
        )
        count += 1

    await db.commit()
    return count
