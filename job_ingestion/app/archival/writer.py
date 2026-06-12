from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from app.config import get_settings


def get_archive_filepath(run_date: datetime | None = None) -> Path:
    date_str = (run_date or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    path = Path(get_settings().archive_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path / f"jobs_{date_str}.jsonl"


def serialize_for_archive(job_archive_row: dict) -> str:
    def default(obj: object) -> object:
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, list):
            return obj
        raise TypeError(f"Not serializable: {type(obj)}")

    return json.dumps(job_archive_row, default=default, ensure_ascii=False)


def write_archive_batch(rows: list[dict], filepath: Path) -> int:
    lines = [serialize_for_archive(row) for row in rows]
    with open(filepath, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    return len(lines)
