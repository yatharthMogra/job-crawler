from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.h1b.fiscal_year import fiscal_year_from_date
from app.ingestion.h1b.wages import normalize_wage_to_annual
from app.models.h1b import LcaRaw

_LCA_COLUMN_ALIASES: dict[str, list[str]] = {
    "employer_name_raw": ["EMPLOYER_NAME", "Employer Name", "EMPLOYER NAME"],
    "soc_code": ["SOC_CODE", "SOC Code"],
    "soc_title": ["SOC_TITLE", "SOC Title"],
    "job_title": ["JOB_TITLE", "Job Title"],
    "wage_from": ["WAGE_RATE_OF_PAY_FROM", "Wage Rate of Pay From", "PREVAILING_WAGE"],
    "wage_unit": ["WAGE_UNIT_OF_PAY", "Wage Unit of Pay", "PW_UNIT_OF_PAY"],
    "worksite_state": ["WORKSITE_STATE", "Worksite State"],
    "worksite_city": ["WORKSITE_CITY", "Worksite City"],
    "case_status": ["CASE_STATUS", "Case Status"],
    "visa_class": ["VISA_CLASS", "Visa Class"],
    "received_date": ["RECEIVED_DATE", "Received Date"],
    "decision_date": ["DECISION_DATE", "Decision Date"],
}


def _resolve_column(df: pd.DataFrame, field: str) -> str | None:
    for candidate in _LCA_COLUMN_ALIASES.get(field, []):
        if candidate in df.columns:
            return candidate
    return None


def _parse_date(value: Any) -> date | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.date()


def _read_lca_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path, dtype=str)
    return pd.read_csv(path, dtype=str, low_memory=False)


def _row_to_lca_record(row: pd.Series, *, source_file: str, columns: dict[str, str]) -> dict[str, Any] | None:
    visa_col = columns.get("visa_class")
    if visa_col:
        visa = str(row.get(visa_col, "") or "").strip().upper()
        if visa and visa != "H-1B":
            return None

    employer_col = columns["employer_name_raw"]
    employer = str(row.get(employer_col, "") or "").strip()
    if not employer:
        return None

    received = _parse_date(row.get(columns.get("received_date", ""))) if columns.get("received_date") else None
    fiscal_year = fiscal_year_from_date(received)
    if fiscal_year is None:
        fiscal_year = fiscal_year_from_date(
            _parse_date(row.get(columns.get("decision_date", ""))) if columns.get("decision_date") else None
        )
    if fiscal_year is None:
        return None

    wage_col = columns.get("wage_from")
    unit_col = columns.get("wage_unit")
    wage_from = None
    if wage_col:
        raw_wage = row.get(wage_col)
        try:
            wage_from = float(str(raw_wage).replace(",", "").replace("$", "")) if raw_wage else None
        except ValueError:
            wage_from = None

    return {
        "employer_name_raw": employer,
        "soc_code": str(row.get(columns["soc_code"], "") or "").strip() or None if columns.get("soc_code") else None,
        "soc_title": str(row.get(columns["soc_title"], "") or "").strip() or None if columns.get("soc_title") else None,
        "job_title": str(row.get(columns["job_title"], "") or "").strip() or None if columns.get("job_title") else None,
        "wage_from": wage_from,
        "wage_unit": str(row.get(unit_col, "") or "").strip() or None if unit_col else None,
        "worksite_state": str(row.get(columns["worksite_state"], "") or "").strip()[:2] or None
        if columns.get("worksite_state")
        else None,
        "worksite_city": str(row.get(columns["worksite_city"], "") or "").strip() or None
        if columns.get("worksite_city")
        else None,
        "case_status": str(row.get(columns["case_status"], "") or "").strip() or None
        if columns.get("case_status")
        else None,
        "visa_class": "H-1B",
        "received_date": received,
        "decision_date": _parse_date(row.get(columns["decision_date"])) if columns.get("decision_date") else None,
        "fiscal_year": fiscal_year,
        "source_file": source_file,
    }


async def load_lca_file(
    db: AsyncSession,
    path: Path,
    *,
    chunk_size: int = 50_000,
) -> dict[str, int]:
    df = _read_lca_file(path)
    columns: dict[str, str] = {}
    for field in _LCA_COLUMN_ALIASES:
        col = _resolve_column(df, field)
        if col:
            columns[field] = col
    if "employer_name_raw" not in columns:
        raise ValueError(f"Could not find employer name column in {path.name}")

    source_file = path.name
    inserted = 0
    skipped = 0
    filtered = 0

    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start : start + chunk_size]
        records: list[dict[str, Any]] = []
        for _, row in chunk.iterrows():
            record = _row_to_lca_record(row, source_file=source_file, columns=columns)
            if record is None:
                filtered += 1
                continue
            records.append(record)

        if not records:
            continue

        stmt = insert(LcaRaw).values(records)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["employer_name_raw", "soc_code", "received_date", "fiscal_year"]
        )
        result = await db.execute(stmt)
        inserted += result.rowcount or 0
        skipped += len(records) - (result.rowcount or 0)

    await db.commit()
    return {"inserted": inserted, "skipped_duplicates": skipped, "filtered_non_h1b": filtered}
