"""Job-anchored skill and capability coverage with lexical and optional semantic matching."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import structlog
from rapidfuzz import fuzz

from app.config import Settings
from app.models.shared import NormalizedJob
from app.scoring.bm25_corpus import bm25_score
from app.scoring.embedding_similarity import calibrate_similarity, cosine_similarity
from app.scoring.text_corpus import collect_protected_phrases, normalize_phrase, tokenize_text
from app.services.profile_loader import UserProfile

log = structlog.get_logger(__name__)

EmbedFn = Callable[[str], list[float] | None]

_DEFAULT_MIN_SIM = 0.3
_DEFAULT_MAX_SIM = 0.85


def flatten_skills(skills: dict[str, Any]) -> list[str]:
    flattened: list[str] = []
    for key in ("languages", "frameworks", "tools", "databases", "other"):
        value = skills.get(key)
        if isinstance(value, list):
            flattened.extend(str(item) for item in value)
    return flattened


def _candidate_skill_terms(profile: UserProfile) -> list[str]:
    return flatten_skills(profile.skills or {})


def _candidate_capability_terms(profile: UserProfile) -> list[str]:
    return [cap.capability_name for cap in profile.capabilities]


def _job_required_skill_terms(job: NormalizedJob) -> list[str]:
    required = list(getattr(job, "required_skills", None) or [])
    if required:
        return required
    fallback = list(dict.fromkeys([*(job.tech_stack or []), *(job.skills or [])]))
    if fallback:
        log.debug(
            "skill_coverage_required_fallback",
            job_id=str(job.id),
            fallback_count=len(fallback),
        )
    return fallback


def _exact_match_score(job_term: str, candidate_terms: list[str]) -> float:
    normalized_job_term = normalize_phrase(job_term)
    if not normalized_job_term:
        return 0.0
    for candidate_term in candidate_terms:
        if normalize_phrase(candidate_term) == normalized_job_term:
            return 1.0
    return 0.0


def _pairwise_bm25_score(
    job_term: str,
    candidate_terms: list[str],
    *,
    idf_by_term: dict[str, float] | None,
    corpus_size: int,
    avg_doc_len: float,
) -> float:
    if not candidate_terms:
        return 0.0
    phrases = collect_protected_phrases([job_term], candidate_terms)
    query_tokens = tokenize_text(job_term, protected_phrases=phrases)
    if not query_tokens:
        return 0.0

    self_score = bm25_score(
        query_tokens,
        query_tokens,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
    )

    best = 0.0
    if self_score > 0:
        combined_doc_tokens: list[str] = []
        for candidate_term in candidate_terms:
            doc_tokens = tokenize_text(candidate_term, protected_phrases=phrases)
            combined_doc_tokens.extend(doc_tokens)
            if not doc_tokens:
                continue
            raw = bm25_score(
                query_tokens,
                doc_tokens,
                idf_by_term=idf_by_term,
                corpus_size=corpus_size,
                avg_doc_len=avg_doc_len,
            )
            best = max(best, raw / self_score)

        if combined_doc_tokens:
            combined_raw = bm25_score(
                query_tokens,
                combined_doc_tokens,
                idf_by_term=idf_by_term,
                corpus_size=corpus_size,
                avg_doc_len=avg_doc_len,
            )
            best = max(best, combined_raw / self_score)

    if best <= 0.0:
        normalized_job = normalize_phrase(job_term)
        for candidate_term in candidate_terms:
            normalized_candidate = normalize_phrase(candidate_term)
            ratio = fuzz.partial_ratio(normalized_job, normalized_candidate) / 100.0
            best = max(best, ratio)

    return max(0.0, min(1.0, best))


def _lookup_embed(
    term: str,
    embed_fn: EmbedFn,
    embed_cache: dict[str, list[float] | None] | None,
) -> list[float] | None:
    key = normalize_phrase(term)
    if embed_cache is not None and key in embed_cache:
        return embed_cache[key]
    vector = embed_fn(term)
    if embed_cache is not None:
        embed_cache[key] = vector
    return vector


def _semantic_match_score(
    job_term: str,
    candidate_terms: list[str],
    *,
    embed_fn: EmbedFn,
    min_sim: float,
    max_sim: float,
    embed_cache: dict[str, list[float] | None] | None = None,
) -> float | None:
    job_vector = _lookup_embed(job_term, embed_fn, embed_cache)
    if not job_vector:
        return None
    best: float | None = None
    for candidate_term in candidate_terms:
        candidate_vector = _lookup_embed(candidate_term, embed_fn, embed_cache)
        if not candidate_vector:
            continue
        raw = cosine_similarity(job_vector, candidate_vector)
        if raw is None or raw <= 0:
            continue
        calibrated = calibrate_similarity(raw, min_sim, max_sim)
        best = calibrated if best is None else max(best, calibrated)
    return best


def best_fuzzy_match(
    job_term: str,
    candidate_terms: list[str],
    *,
    settings: Settings,
    embed_fn: EmbedFn | None = None,
    embedding_min_sim: float = _DEFAULT_MIN_SIM,
    embedding_max_sim: float = _DEFAULT_MAX_SIM,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = 400.0,
    embed_cache: dict[str, list[float] | None] | None = None,
) -> float:
    if not job_term.strip():
        return 0.0
    if not candidate_terms:
        return 0.0

    exact = _exact_match_score(job_term, candidate_terms)
    if exact >= 1.0:
        return 1.0

    bm25 = _pairwise_bm25_score(
        job_term,
        candidate_terms,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
    )

    semantic: float | None = None
    if embed_fn is not None:
        semantic = _semantic_match_score(
            job_term,
            candidate_terms,
            embed_fn=embed_fn,
            min_sim=embedding_min_sim,
            max_sim=embedding_max_sim,
            embed_cache=embed_cache,
        )

    bm25_w = settings.coverage_fuzzy_bm25_weight
    semantic_w = settings.coverage_fuzzy_semantic_weight if semantic is not None else 0.0
    total = bm25_w + semantic_w
    if total <= 0:
        return max(exact, bm25)
    semantic_value = semantic if semantic is not None else 0.0
    blended = (bm25_w * bm25 + semantic_w * semantic_value) / total
    return max(exact, min(1.0, blended))


def _average_term_coverage(
    job_terms: list[str],
    candidate_terms: list[str],
    *,
    settings: Settings,
    embed_fn: EmbedFn | None = None,
    embedding_min_sim: float = _DEFAULT_MIN_SIM,
    embedding_max_sim: float = _DEFAULT_MAX_SIM,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = 400.0,
    embed_cache: dict[str, list[float] | None] | None = None,
) -> float:
    if not job_terms:
        return 1.0
    if not candidate_terms:
        return 0.0
    total = sum(
        best_fuzzy_match(
            term,
            candidate_terms,
            settings=settings,
            embed_fn=embed_fn,
            embedding_min_sim=embedding_min_sim,
            embedding_max_sim=embedding_max_sim,
            idf_by_term=idf_by_term,
            corpus_size=corpus_size,
            avg_doc_len=avg_doc_len,
            embed_cache=embed_cache,
        )
        for term in job_terms
    )
    return total / len(job_terms)


def skill_coverage_components(
    job: NormalizedJob,
    profile: UserProfile,
    settings: Settings,
    *,
    embed_fn: EmbedFn | None = None,
    embedding_min_sim: float = _DEFAULT_MIN_SIM,
    embedding_max_sim: float = _DEFAULT_MAX_SIM,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = 400.0,
    embed_cache: dict[str, list[float] | None] | None = None,
) -> tuple[float, float, float]:
    candidate_terms = _candidate_skill_terms(profile)
    required_terms = _job_required_skill_terms(job)
    preferred_terms = list(getattr(job, "preferred_skills", None) or [])

    required_cov = _average_term_coverage(
        required_terms,
        candidate_terms,
        settings=settings,
        embed_fn=embed_fn,
        embedding_min_sim=embedding_min_sim,
        embedding_max_sim=embedding_max_sim,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
        embed_cache=embed_cache,
    )
    preferred_cov = _average_term_coverage(
        preferred_terms,
        candidate_terms,
        settings=settings,
        embed_fn=embed_fn,
        embedding_min_sim=embedding_min_sim,
        embedding_max_sim=embedding_max_sim,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
        embed_cache=embed_cache,
    )
    combined = (
        settings.qualification_fit_required_skill_weight * required_cov
        + settings.qualification_fit_preferred_skill_weight * preferred_cov
    )
    return combined, required_cov, preferred_cov


def skill_coverage(
    job: NormalizedJob,
    profile: UserProfile,
    settings: Settings,
    *,
    embed_fn: EmbedFn | None = None,
    embedding_min_sim: float = _DEFAULT_MIN_SIM,
    embedding_max_sim: float = _DEFAULT_MAX_SIM,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = 400.0,
    embed_cache: dict[str, list[float] | None] | None = None,
) -> float:
    combined, _, _ = skill_coverage_components(
        job,
        profile,
        settings,
        embed_fn=embed_fn,
        embedding_min_sim=embedding_min_sim,
        embedding_max_sim=embedding_max_sim,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
        embed_cache=embed_cache,
    )
    return combined


def capability_coverage(
    job: NormalizedJob,
    profile: UserProfile,
    settings: Settings,
    *,
    embed_fn: EmbedFn | None = None,
    embedding_min_sim: float = _DEFAULT_MIN_SIM,
    embedding_max_sim: float = _DEFAULT_MAX_SIM,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = 400.0,
    embed_cache: dict[str, list[float] | None] | None = None,
) -> float:
    job_caps = list(job.job_capabilities or [])
    if not job_caps:
        return 1.0
    candidate_terms = _candidate_capability_terms(profile)
    return _average_term_coverage(
        job_caps,
        candidate_terms,
        settings=settings,
        embed_fn=embed_fn,
        embedding_min_sim=embedding_min_sim,
        embedding_max_sim=embedding_max_sim,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
        embed_cache=embed_cache,
    )
