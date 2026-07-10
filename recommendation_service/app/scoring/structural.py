from __future__ import annotations

import math
import re
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
