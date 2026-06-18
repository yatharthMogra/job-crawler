"""Persist operator acknowledgements for taxonomy health flagged domains."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_ACK_PATH = Path(__file__).resolve().parents[2] / "data" / "taxonomy_health_ack.json"


def _read_raw() -> dict[str, str]:
    if not _ACK_PATH.exists():
        return {}
    try:
        data = json.loads(_ACK_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def _write_raw(data: dict[str, str]) -> None:
    _ACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    _ACK_PATH.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def list_acknowledged_domains() -> dict[str, str]:
    """Return domain -> ISO timestamp when acknowledged."""
    return _read_raw()


def set_domain_acknowledged(domain: str, *, acknowledged: bool) -> dict[str, str]:
    data = _read_raw()
    if acknowledged:
        data[domain] = datetime.now(timezone.utc).isoformat()
    else:
        data.pop(domain, None)
    _write_raw(data)
    return data
