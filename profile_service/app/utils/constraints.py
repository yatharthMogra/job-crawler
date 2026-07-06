from __future__ import annotations

from typing import Any

_SPONSORSHIP_VISA_TYPES = frozenset(
    {
        "F1",
        "F-1",
        "OPT",
        "CPT",
        "H1B",
        "H-1B",
        "H4",
        "H-4",
        "J1",
        "J-1",
        "L1",
        "L-1",
        "TN",
    }
)

_SPONSORSHIP_WORK_AUTH = frozenset(
    {
        "F1",
        "F-1",
        "OPT",
        "CPT",
        "H1B",
        "H-1B",
        "H4",
        "H-4",
        "J1",
        "J-1",
        "L1",
        "L-1",
        "TN",
        "OTHER_VISA",
        "NEEDS_SPONSORSHIP",
    }
)


def _normalized(value: object) -> str:
    return str(value or "").strip().upper().replace(" ", "_").replace("-", "_")


def normalize_constraints(constraints: dict[str, Any]) -> dict[str, Any]:
    """Derive hard recommendation filters from EEO and work-authorization signals."""
    normalized = dict(constraints)
    eeo = normalized.get("eeo")
    if isinstance(eeo, dict) and eeo.get("requires_sponsorship") is True:
        normalized["sponsorship_required"] = True

    visa_type = _normalized(normalized.get("visa_type")).replace("__", "_")
    work_auth = _normalized(normalized.get("work_authorization")).replace("__", "_")
    if visa_type in _SPONSORSHIP_VISA_TYPES or work_auth in _SPONSORSHIP_WORK_AUTH:
        normalized["sponsorship_required"] = True

    return normalized
