from __future__ import annotations

import math
from typing import TYPE_CHECKING

from app.scoring.text_corpus import tokenize_text

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

BM25_K1 = 1.5
BM25_B = 0.75
DEFAULT_AVG_DOC_LEN = 400.0


_idf_cache: dict[str, float] = {}
_corpus_size_cache: int = 0
_avg_doc_len_cache: float = 400.0


def set_idf_cache(idf_by_term: dict[str, float], corpus_size: int, avg_doc_len: float) -> None:
    global _idf_cache, _corpus_size_cache, _avg_doc_len_cache
    _idf_cache = idf_by_term
    _corpus_size_cache = corpus_size
    _avg_doc_len_cache = avg_doc_len


async def load_idf_cache(db: AsyncSession) -> None:
    from sqlalchemy import select

    from app.models.shared import JobTermIdf

    rows = (await db.scalars(select(JobTermIdf))).all()
    if not rows:
        set_idf_cache({}, 0, DEFAULT_AVG_DOC_LEN)
        return
    corpus_size = rows[0].corpus_size
    idf_by_term = {row.term: row.idf for row in rows}
    avg_doc_len = sum(row.document_frequency for row in rows) / max(len(rows), 1)
    set_idf_cache(idf_by_term, corpus_size, float(avg_doc_len))


def _term_idf(term: str, idf_by_term: dict[str, float], corpus_size: int) -> float:
    if term in idf_by_term:
        return idf_by_term[term]
    if corpus_size <= 0:
        return 0.0
    return math.log(1.0 + (corpus_size - 0.5) / 1.5)


def bm25_score(
    query_tokens: list[str],
    doc_tokens: list[str],
    *,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = DEFAULT_AVG_DOC_LEN,
) -> float:
    if not query_tokens or not doc_tokens:
        return 0.0
    if idf_by_term is None:
        idf_by_term, corpus_size, avg_doc_len = _idf_cache, _corpus_size_cache, _avg_doc_len_cache

    doc_len = len(doc_tokens)
    if doc_len == 0:
        return 0.0

    term_freq = {}
    for token in doc_tokens:
        term_freq[token] = term_freq.get(token, 0) + 1

    score = 0.0
    for term in set(query_tokens):
        tf = term_freq.get(term, 0)
        if tf == 0:
            continue
        idf = _term_idf(term, idf_by_term, corpus_size)
        numerator = tf * (BM25_K1 + 1)
        denominator = tf + BM25_K1 * (1 - BM25_B + BM25_B * (doc_len / max(avg_doc_len, 1.0)))
        score += idf * (numerator / denominator)
    return score


def _token_overlap_score(resume_tokens: list[str], job_tokens: list[str]) -> float:
    if not resume_tokens or not job_tokens:
        return 0.0
    resume_set = set(resume_tokens)
    job_set = set(job_tokens)
    overlap = len(resume_set & job_set)
    return overlap / max(len(job_set), 1)


def normalized_bm25_score(
    resume_text: str,
    job_text: str,
    *,
    protected_phrases: list[str] | None = None,
    idf_by_term: dict[str, float] | None = None,
    corpus_size: int = 0,
    avg_doc_len: float = DEFAULT_AVG_DOC_LEN,
) -> float:
    phrases = protected_phrases or []
    resume_tokens = tokenize_text(resume_text, protected_phrases=phrases)
    job_tokens_list = tokenize_text(job_text, protected_phrases=phrases)
    if not resume_tokens or not job_tokens_list:
        return 0.0

    if idf_by_term is None:
        idf_by_term, corpus_size, avg_doc_len = _idf_cache, _corpus_size_cache, _avg_doc_len_cache
    if not idf_by_term:
        return _token_overlap_score(resume_tokens, job_tokens_list)

    resume_on_job = bm25_score(
        resume_tokens,
        job_tokens_list,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
    )
    job_on_job = bm25_score(
        job_tokens_list,
        job_tokens_list,
        idf_by_term=idf_by_term,
        corpus_size=corpus_size,
        avg_doc_len=avg_doc_len,
    )
    if job_on_job <= 0:
        return 0.0
    return max(0.0, min(1.0, resume_on_job / job_on_job))
