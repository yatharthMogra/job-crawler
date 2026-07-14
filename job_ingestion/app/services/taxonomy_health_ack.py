"""Persist operator acknowledgements for taxonomy health flagged groups."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

GroupBy = Literal["domain", "role"]

_ACK_PATH = Path(__file__).resolve().parents[2] / "data" / "taxonomy_health_ack.json"


def _empty() -> dict[str, dict[str, str]]:
    return {"domains": {}, "roles": {}}


def _read_store() -> dict[str, dict[str, str]]:
    if not _ACK_PATH.exists():
        return _empty()
    try:
        data = json.loads(_ACK_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return _empty()
    if not isinstance(data, dict):
        return _empty()

    # Legacy flat format: { "Business": "2026-..." }
    if "domains" not in data and "roles" not in data:
        return {
            "domains": {str(k): str(v) for k, v in data.items()},
            "roles": {},
        }

    domains = data.get("domains") if isinstance(data.get("domains"), dict) else {}
    roles = data.get("roles") if isinstance(data.get("roles"), dict) else {}
    return {
        "domains": {str(k): str(v) for k, v in domains.items()},
        "roles": {str(k): str(v) for k, v in roles.items()},
    }


def _write_store(store: dict[str, dict[str, str]]) -> None:
    _ACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "domains": dict(sorted(store.get("domains", {}).items())),
        "roles": dict(sorted(store.get("roles", {}).items())),
    }
    _ACK_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def list_acknowledged_domains() -> dict[str, str]:
    """Return domain -> ISO timestamp when acknowledged."""
    return _read_store()["domains"]


def list_acknowledged_roles() -> dict[str, str]:
    """Return role -> ISO timestamp when acknowledged."""
    return _read_store()["roles"]


def list_acknowledgements(group_by: GroupBy) -> dict[str, str]:
    return list_acknowledged_roles() if group_by == "role" else list_acknowledged_domains()


def set_domain_acknowledged(domain: str, *, acknowledged: bool) -> dict[str, str]:
    return set_group_acknowledged("domain", domain, acknowledged=acknowledged)


def set_group_acknowledged(group_by: GroupBy, key: str, *, acknowledged: bool) -> dict[str, str]:
    store = _read_store()
    bucket = "roles" if group_by == "role" else "domains"
    if acknowledged:
        store[bucket][key] = datetime.now(timezone.utc).isoformat()
    else:
        store[bucket].pop(key, None)
    _write_store(store)
    return store[bucket]
