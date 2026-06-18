from __future__ import annotations

import re

LEGAL_SUFFIXES = [
    r"\bLLC\b",
    r"\bINC\b",
    r"\bINC\.\b",
    r"\bCORP\b",
    r"\bCORPORATION\b",
    r"\bLTD\b",
    r"\bL\.P\.\b",
    r"\bLP\b",
    r"\bLLP\b",
    r"\bPLC\b",
    r"\bCO\b",
    r"\bCO\.\b",
    r"\bGROUP\b",
    r"\bHOLDINGS\b",
    r"\bHOLDING\b",
    r"\bENTERPRISES\b",
    r"\bSOLUTIONS\b",
    r"\bSERVICES\b",
    r"\bTECHNOLOGIES\b",
    r"\bTECHNOLOGY\b",
]

GEO_SUFFIXES = [
    r"\bUSA\b",
    r"\bUS\b",
    r"\bU\.S\.\b",
    r"\bAMERICA\b",
    r"\bNORTH AMERICA\b",
    r"\bAMERICAS\b",
]


def normalize_employer_name(raw: str) -> str:
    name = raw.upper().strip()
    name = re.sub(r"[^\w\s\-]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    prev = None
    while prev != name:
        prev = name
        for suffix in LEGAL_SUFFIXES:
            name = re.sub(suffix, "", name).strip()
    for geo in GEO_SUFFIXES:
        name = re.sub(geo, "", name).strip()
    name = re.sub(r"\s+", " ", name).strip()
    return name
