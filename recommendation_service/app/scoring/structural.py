from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from rapidfuzz import fuzz

from app.models.shared import CandidateEvidence, NormalizedJob
from app.scoring.experience_tier import experience_tier_distance_score
from app.services.profile_loader import UserProfile

_DEGREE_RANK = {
    "high_school": 1,
    "associate": 2,
    "bachelor": 3,
    "bs": 3,
    "ba": 3,
    "bsc": 3,
    "master": 4,
    "ms": 4,
    "mba": 4,
    "ma": 4,
    "msc": 4,
    "phd": 5,
    "doctorate": 5,
}

_DEGREE_PATTERNS: list[tuple[re.Pattern[str], int]] = [
    (re.compile(r"\bph\.?d\b", re.I), 5),
    (re.compile(r"\bdoctorate\b", re.I), 5),
    (re.compile(r"\bmaster'?s?\b", re.I), 4),
    (re.compile(r"\bmba\b", re.I), 4),
    (re.compile(r"\bm\.?s\.?\b", re.I), 4),
    (re.compile(r"\bbachelor'?s?\b", re.I), 3),
    (re.compile(r"\bb\.?s\.?\b", re.I), 3),
    (re.compile(r"\bb\.?a\.?\b", re.I), 3),
]


def _highest_degree_rank(education: dict[str, Any]) -> int | None:
    ranks: list[int] = []
    entries = education.get("entries") or []
    for entry in entries:
        degree = str(entry.get("degree") or "")
        rank = _degree_text_rank(degree)
        if rank is not None:
            ranks.append(rank)
    legacy_degree = str(education.get("degree") or "")
    legacy_rank = _degree_text_rank(legacy_degree)
    if legacy_rank is not None:
        ranks.append(legacy_rank)
    return max(ranks) if ranks else None


def _degree_text_rank(text: str) -> int | None:
    lowered = text.lower()
    for token, rank in _DEGREE_RANK.items():
        if token in lowered:
            return rank
    return None


_YEARS_PATTERN = re.compile(r"(\d+)\+?\s*years?", re.I)
_DATE_VALUE_RE = re.compile(r"^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?$")


def _parse_evidence_date(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not cleaned or cleaned.lower() in {"present", "current", "now"}:
        return datetime.now(UTC)
    match = _DATE_VALUE_RE.match(cleaned)
    if not match:
        return None
    year = int(match.group(1))
    month = int(match.group(2) or 1)
    day = int(match.group(3) or 1)
    try:
        return datetime(year, month, day, tzinfo=UTC)
    except ValueError:
        return None


def _months_between(start: datetime, end: datetime) -> int:
    if end < start:
        return 0
    return max(0, (end.year - start.year) * 12 + (end.month - start.month))


def infer_required_experience_years(job: NormalizedJob) -> int | None:
    text = "\n".join(job.required_qualifications or [])
    matches = [int(match.group(1)) for match in _YEARS_PATTERN.finditer(text)]
    return max(matches) if matches else None


def _infer_experience_months_from_evidence(evidence: list[CandidateEvidence]) -> int:
    total_months = 0
    for item in evidence:
        if item.evidence_type != "experience" or not item.is_active or not item.is_approved:
            continue
        data = item.normalized_data or {}
        start = _parse_evidence_date(data.get("start_date"))
        end = _parse_evidence_date(data.get("end_date"))
        if start and end:
            total_months += _months_between(start, end)
            continue
        duration_months = data.get("duration_months")
        if isinstance(duration_months, (int, float)) and duration_months > 0:
            total_months += int(duration_months)
    return total_months


def infer_candidate_experience_years(profile: UserProfile) -> float | None:
    constraints = profile.constraints or {}
    years = constraints.get("full_time_experience_years")
    if years is not None:
        try:
            return float(years)
        except (TypeError, ValueError):
            return None
    evidence_months = _infer_experience_months_from_evidence(profile.evidence)
    if evidence_months > 0:
        return round(evidence_months / 12.0, 1)
    return None


def experience_adequacy_score(profile: UserProfile, job: NormalizedJob) -> float:
    required_years = infer_required_experience_years(job)
    if required_years is None:
        return 1.0
    candidate_years = infer_candidate_experience_years(profile)
    if candidate_years is None:
        return 0.5
    if candidate_years >= required_years:
        return 1.0
    return max(0.0, candidate_years / required_years)


def qualification_structural_score(profile: UserProfile, job: NormalizedJob) -> float:
    experience = experience_adequacy_score(profile, job)
    education = education_adequacy_score(profile, job)
    return (experience + education) / 2.0


def infer_required_degree_rank(job: NormalizedJob) -> int | None:
    text = "\n".join(job.required_qualifications or [])
    ranks = [rank for pattern, rank in _DEGREE_PATTERNS if pattern.search(text)]
    return max(ranks) if ranks else None


def education_alignment_score(profile: UserProfile, job: NormalizedJob) -> float:
    candidate_rank = _highest_degree_rank(profile.education or {})
    required_rank = infer_required_degree_rank(job)
    if candidate_rank is None or required_rank is None:
        return 0.5
    if candidate_rank >= required_rank:
        return 1.0
    gap = required_rank - candidate_rank
    return max(0.0, 1.0 - 0.25 * gap)


def education_adequacy_score(profile: UserProfile, job: NormalizedJob) -> float:
    required_rank = infer_required_degree_rank(job)
    if required_rank is None:
        return 1.0
    candidate_rank = _highest_degree_rank(profile.education or {})
    if candidate_rank is None:
        return 0.5
    if candidate_rank >= required_rank:
        return 1.0
    return max(0.0, 1.0 - 0.25 * (required_rank - candidate_rank))


def _most_recent_experience_title(evidence: list[CandidateEvidence]) -> str | None:
    titles: list[str] = []
    for item in evidence:
        if item.evidence_type != "experience" or not item.is_active or not item.is_approved:
            continue
        title = str((item.normalized_data or {}).get("title") or "").strip()
        if title:
            titles.append(title)
    return titles[0] if titles else None


def title_similarity_score(job: NormalizedJob, evidence: list[CandidateEvidence]) -> float:
    candidate_title = _most_recent_experience_title(evidence)
    if not candidate_title:
        return 0.5
    ratio = fuzz.token_sort_ratio(candidate_title, job.title) / 100.0
    return max(0.0, min(1.0, ratio))


def experience_alignment_score(profile: UserProfile, job: NormalizedJob) -> float:
    constraints = profile.constraints or {}
    return experience_tier_distance_score(
        job.experience_tier,
        constraints.get("current_experience_tier"),
    )


def structural_match_score(profile: UserProfile, job: NormalizedJob) -> float:
    title = title_similarity_score(job, profile.evidence)
    experience = experience_alignment_score(profile, job)
    education = education_alignment_score(profile, job)
    return (title * 0.35) + (experience * 0.40) + (education * 0.25)


def structural_signal_breakdown(profile: UserProfile, job: NormalizedJob) -> dict[str, float]:
    return {
        "title": title_similarity_score(job, profile.evidence),
        "experience": experience_alignment_score(profile, job),
        "education": education_alignment_score(profile, job),
    }
