from __future__ import annotations

import tempfile
from pathlib import Path

from app.ingestion.h1b.load_lca import _read_lca_file, _row_to_lca_record


def test_lca_row_parses_h1b_only() -> None:
    csv_content = (
        "EMPLOYER_NAME,SOC_CODE,SOC_TITLE,JOB_TITLE,WAGE_RATE_OF_PAY_FROM,"
        "WAGE_UNIT_OF_PAY,WORKSITE_STATE,WORKSITE_CITY,CASE_STATUS,VISA_CLASS,"
        "RECEIVED_DATE,DECISION_DATE\n"
        "Google LLC,15-1252,Software Developers,SWE,150000,Year,CA,Mountain View,"
        "Certified,H-1B,2024-03-15,2024-04-01\n"
        "Acme Corp,15-1252,Software Developers,SWE,100,Hour,NY,New York,"
        "Certified,H-1B,2024-05-01,2024-06-01\n"
        "No Visa Co,15-1252,Software Developers,SWE,100000,Year,TX,Austin,"
        "Certified,E-3,2024-05-01,2024-06-01\n"
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        tmp.write(csv_content)
        path = Path(tmp.name)

    try:
        df = _read_lca_file(path)
        columns = {}
        from app.ingestion.h1b.load_lca import _LCA_COLUMN_ALIASES, _resolve_column

        for field in _LCA_COLUMN_ALIASES:
            col = _resolve_column(df, field)
            if col:
                columns[field] = col

        records = [
            _row_to_lca_record(row, source_file=path.name, columns=columns)
            for _, row in df.iterrows()
        ]
        valid = [r for r in records if r is not None]
        assert len(valid) == 2
        assert valid[0]["employer_name_raw"] == "Google LLC"
        assert valid[1]["wage_from"] == 100
        assert valid[1]["wage_unit"] == "Hour"
    finally:
        path.unlink()
