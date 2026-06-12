"""Job country extraction for location scoring (mirrors job_ingestion deterministic logic)."""

from __future__ import annotations

COUNTRY_SIGNALS: list[tuple[list[str], str | None]] = [
    (
        ["canada", ", on", ", bc", ", qc", "ontario", "british columbia", "toronto", "montreal", "vancouver"],
        "CA",
    ),
    (
        [
            "united states",
            "usa",
            "u.s.a",
            " us ",
            "remote - us",
            "remote - united",
        ],
        "US",
    ),
    (
        ["united kingdom", " uk", "england", "london", "manchester", "edinburgh", "bristol"],
        "GB",
    ),
    (
        ["germany", "deutschland", "berlin", "munich", "hamburg", "frankfurt"],
        "DE",
    ),
    (
        [
            "india",
            "bengaluru",
            "hyderabad",
            "bangalore",
            "pune",
            "chennai",
            "mumbai",
            "new delhi",
            "gurgaon",
            "noida",
        ],
        "IN",
    ),
    (
        ["australia", "sydney", "melbourne", "brisbane", "perth"],
        "AU",
    ),
    (
        [
            "new york",
            "san francisco",
            "seattle",
            "boston",
            "chicago",
            "los angeles",
            "austin",
            "denver",
            "atlanta",
            "washington, d.c",
            ", ny",
            ", ca",
            ", wa",
            ", tx",
            ", ma",
            ", co",
            ", ga",
            ", fl",
            ", va",
            ", dc",
            ", nc",
            ", il",
            ", oh",
            ", pa",
            ", az",
            ", mn",
        ],
        "US",
    ),
    (
        ["remote", "anywhere", "worldwide", "global"],
        None,
    ),
]

US_AUTH_TYPES = frozenset(
    {
        "US_CITIZEN",
        "PERMANENT_RESIDENT",
        "GREEN_CARD",
        "OPT",
        "CPT",
        "H1B",
        "TN",
        "OTHER_US",
        "CPT_OPT",
    }
)


def extract_job_country(location: str | None) -> str | None:
    if not location:
        return None
    stripped = location.lower().strip()
    if stripped.startswith("us-") or stripped.startswith("us,"):
        return "US"
    loc_lower = f" {stripped} "

    if any(sig in loc_lower for sig in ["remote", "anywhere", "worldwide", "global"]):
        return None

    for signals, code in COUNTRY_SIGNALS:
        if code is None:
            continue
        if any(sig in loc_lower for sig in signals):
            return code

    return None


def get_effective_countries(preferences: dict, constraints: dict) -> list[str]:
    preferred = preferences.get("preferred_countries") or []
    if preferred:
        return [str(c).upper() for c in preferred if c]

    work_auth = constraints.get("work_authorization")
    if work_auth and str(work_auth).upper() in US_AUTH_TYPES:
        return ["US"]

    return []
