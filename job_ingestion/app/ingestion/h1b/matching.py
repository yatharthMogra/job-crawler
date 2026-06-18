from __future__ import annotations

import uuid
from dataclasses import dataclass

from rapidfuzz import fuzz, process
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.h1b.normalize import normalize_employer_name
from app.models.company import Company
from app.models.h1b import H1bEmployer, H1bEmployerAlias


@dataclass
class MatchResult:
    company_id: uuid.UUID | None
    match_method: str
    match_confidence: float
    matched_norm_name: str | None = None


def fuzzy_match_employer(
    norm_name: str,
    company_lookup: dict[str, uuid.UUID],
) -> tuple[str | None, float]:
    """Return (matched_norm_name, confidence 0-1) or (None, 0.0)."""
    result = process.extractOne(
        norm_name,
        company_lookup.keys(),
        scorer=fuzz.token_sort_ratio,
        score_cutoff=75,
    )
    if result is None:
        return None, 0.0
    match_name, score, _ = result
    return match_name, score / 100.0


def classify_fuzzy_match(confidence: float) -> str:
    if confidence >= 0.88:
        return "fuzzy_auto"
    if confidence >= 0.75:
        return "fuzzy_candidate"
    return "unmatched"


async def build_company_lookup(db: AsyncSession) -> dict[str, uuid.UUID]:
    result = await db.execute(select(Company.id, Company.name))
    lookup: dict[str, uuid.UUID] = {}
    for company_id, name in result.all():
        norm = normalize_employer_name(name)
        if norm and norm not in lookup:
            lookup[norm] = company_id
    return lookup


async def match_employer(
    db: AsyncSession,
    raw_name: str,
    *,
    company_lookup: dict[str, uuid.UUID] | None = None,
) -> MatchResult:
    norm_name = normalize_employer_name(raw_name)
    if not norm_name:
        return MatchResult(None, "unmatched", 0.0)

    lookup = company_lookup or await build_company_lookup(db)

    if norm_name in lookup:
        return MatchResult(lookup[norm_name], "exact", 1.0, norm_name)

    matched_norm, confidence = fuzzy_match_employer(norm_name, lookup)
    method = classify_fuzzy_match(confidence)
    if method == "fuzzy_auto" and matched_norm:
        return MatchResult(lookup[matched_norm], method, confidence, matched_norm)
    if method == "fuzzy_candidate":
        return MatchResult(None, method, confidence, matched_norm)
    return MatchResult(None, "unmatched", 0.0)


async def upsert_employer_alias(
    db: AsyncSession,
    *,
    raw_name: str,
    norm_name: str,
    first_seen_year: int | None,
    match: MatchResult,
) -> H1bEmployer:
    employer = await db.scalar(
        select(H1bEmployer).where(H1bEmployer.employer_name_norm == norm_name)
    )
    if employer is None:
        employer = H1bEmployer(
            employer_name_norm=norm_name,
            company_id=match.company_id,
            match_method=match.match_method,
            match_confidence=match.match_confidence,
        )
        db.add(employer)
    elif match.company_id and employer.company_id is None and match.match_method in (
        "exact",
        "fuzzy_auto",
        "manual",
    ):
        employer.company_id = match.company_id
        employer.match_method = match.match_method
        employer.match_confidence = match.match_confidence

    alias = await db.get(H1bEmployerAlias, raw_name)
    if alias is None:
        db.add(
            H1bEmployerAlias(
                employer_name_raw=raw_name,
                employer_name_norm=norm_name,
                first_seen_year=first_seen_year,
            )
        )

    return employer
