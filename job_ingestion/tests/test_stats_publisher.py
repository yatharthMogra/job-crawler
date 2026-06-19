from __future__ import annotations

import json
from pathlib import Path

from app.ingestion.stats_publisher import write_stats_file


def test_write_stats_file_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "ingestion_stats.json"
    payload = {"generated_at": "2026-06-19T00:00:00+00:00", "jobs": {"active": 10}}
    write_stats_file(payload, path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded == payload
