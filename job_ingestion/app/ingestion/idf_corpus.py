from __future__ import annotations

import math
from collections import Counter
from datetime import UTC, datetime

import structlog
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_term_idf import JobTermIdf
from app.models.normalized_job import NormalizedJob
from app.scoring.text_corpus import job_tokens

log = structlog.get_logger(__name__)

BM25_K1 = 1.5
BM25_B = 0.75


def compute_idf(term_df: int, corpus_size: int) -> float:
    if corpus_size <= 0 or term_df <= 0:
        return 0.0
    return math.log(1.0 + (corpus_size - term_df + 0.5) / (term_df + 0.5))


async def build_idf_corpus(db: AsyncSession) -> dict[str, int]:
    jobs = (
        await db.scalars(
            select(NormalizedJob).where(
                NormalizedJob.is_active.is_(True),
                NormalizedJob.processing_state == "success",
            )
        )
    ).all()
    if not jobs:
        log.warning("idf_corpus_empty")
        return {"jobs": 0, "terms": 0}

    document_frequencies: Counter[str] = Counter()
    doc_lengths: list[int] = []
    for job in jobs:
        tokens = job_tokens(job)
        if not tokens:
            continue
        doc_lengths.append(len(tokens))
        document_frequencies.update(set(tokens))

    corpus_size = len(doc_lengths)
    if corpus_size == 0:
        return {"jobs": len(jobs), "terms": 0}

    now = datetime.now(UTC)
    await db.execute(delete(JobTermIdf))
    rows = [
        JobTermIdf(
            term=term,
            document_frequency=df,
            idf=compute_idf(df, corpus_size),
            corpus_size=corpus_size,
            updated_at=now,
        )
        for term, df in document_frequencies.items()
    ]
    db.add_all(rows)
    await db.commit()
    log.info("idf_corpus_built", jobs=corpus_size, terms=len(rows))
    return {"jobs": corpus_size, "terms": len(rows)}
