from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.h1b import UscisRaw

_USCIS_COLUMN_ALIASES: dict[str, list[str]] = {
    "employer_name_raw": ["Employer", "EMPLOYER", "Employer Name"],
    "naics_code": ["NAICS", "Naics"],
    "fiscal_year": ["Fiscal Year", "FISCAL_YEAR", "FY"],
    "initial_approvals": ["Initial Approvals", "Initial Approval"],
    "initial_denials": ["Initial Denials", "Initial Denial"],
    "continuing_approvals": ["Continuing Approvals", "Continuing Approval"],
    "continuing_denials": ["Continuing Denials", "Continuing Denial"],
}


def _resolve_column(df: pd.DataFrame, field: str) -> str | None:
    for candidate in _USCIS_COLUMN_ALIASES.get(field, []):
        if candidate in df.columns:
            return candidate
    return None


def _to_int(value: Any) -> int:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return 0
    try:
        return int(float(str(value).replace(",", "")))
    except ValueError:
        return 0


def _read_uscis_file(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, low_memory=False)


async def load_uscis_file(
    db: AsyncSession,
    path: Path,
    *,
    default_fiscal_year: int | None = None,
) -> dict[str, int]:
    df = _read_uscis_file(path)
    columns: dict[str, str] = {}
    for field in _USCIS_COLUMN_ALIASES:
        col = _resolve_column(df, field)
        if col:
            columns[field] = col
    if "employer_name_raw" not in columns:
        raise ValueError(f"Could not find employer column in {path.name}")

    source_file = path.name
    records: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        employer = str(row.get(columns["employer_name_raw"], "") or "").strip()
        if not employer:
            continue
        fy_col = columns.get("fiscal_year")
        fiscal_year = _to_int(row.get(fy_col)) if fy_col else (default_fiscal_year or 0)
        if fiscal_year <= 0:
            continue
        records.append(
            {
                "employer_name_raw": employer,
                "naics_code": str(row.get(columns["naics_code"], "") or "").strip() or None
                if columns.get("naics_code")
                else None,
                "fiscal_year": fiscal_year,
                "initial_approvals": _to_int(row.get(columns.get("initial_approvals", ""))),
                "initial_denials": _to_int(row.get(columns.get("initial_denials", ""))),
                "continuing_approvals": _to_int(row.get(columns.get("continuing_approvals", ""))),
                "continuing_denials": _to_int(row.get(columns.get("continuing_denials", ""))),
                "source_file": source_file,
            }
        )

    if not records:
        return {"inserted": 0, "skipped_duplicates": 0}

    stmt = insert(UscisRaw).values(records)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["employer_name_raw", "fiscal_year", "naics_code"]
    )
    result = await db.execute(stmt)
    await db.commit()
    inserted = result.rowcount or 0
    return {"inserted": inserted, "skipped_duplicates": len(records) - inserted}
