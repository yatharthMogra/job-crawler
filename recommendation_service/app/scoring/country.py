"""Job country extraction for location scoring (mirrors job_ingestion deterministic logic)."""

from __future__ import annotations

import re

COUNTRY_SIGNALS: list[tuple[list[str], str | None]] = [
    (
        ["canada", "ontario", "british columbia", "toronto", "montreal", "vancouver"],
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
    (["singapore"], "SG"),
    (["hong kong"], "HK"),
    (["japan", "tokyo", "osaka"], "JP"),
    (["china", "beijing", "shanghai"], "CN"),
    (["taiwan", "taipei"], "TW"),
    (["south korea", "seoul"], "KR"),
    (["france", "paris"], "FR"),
    (["netherlands", "amsterdam"], "NL"),
    (["switzerland", "zurich"], "CH"),
    (["ireland", "dublin"], "IE"),
    (["israel", "tel aviv"], "IL"),
    (["brazil", "são paulo", "sao paulo"], "BR"),
    (["mexico"], "MX"),
    (["poland", "warsaw"], "PL"),
    (["philippines", "manila"], "PH"),
    (["malaysia", "kuala lumpur"], "MY"),
    (["thailand", "bangkok"], "TH"),
    (["vietnam"], "VN"),
    (["indonesia", "jakarta"], "ID"),
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
        ],
        "US",
    ),
    (
        ["remote", "anywhere", "worldwide", "global"],
        None,
    ),
]

_US_STATE_ABBRS = ("ny", "ca", "wa", "tx", "ma", "co", "ga", "fl", "va", "dc", "nc", "il", "oh", "pa", "az", "mn")
_CA_PROV_ABBRS = ("on", "bc", "qc")


def _matches_abbr_after_comma(loc_lower: str, abbr: str) -> bool:
    pattern = r",\s*" + re.escape(abbr) + r"(?:\s|,|\)|$)"
    return bool(re.search(pattern, loc_lower))

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

    if any(_matches_abbr_after_comma(loc_lower, abbr) for abbr in _US_STATE_ABBRS):
        return "US"
    if any(_matches_abbr_after_comma(loc_lower, abbr) for abbr in _CA_PROV_ABBRS):
        return "CA"

    return None


def get_effective_countries(preferences: dict, constraints: dict) -> list[str]:
    preferred = preferences.get("preferred_countries") or []
    if preferred:
        return [str(c).upper() for c in preferred if c]

    work_auth = constraints.get("work_authorization")
    if work_auth and str(work_auth).upper() in US_AUTH_TYPES:
        return ["US"]

    return []
