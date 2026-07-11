from __future__ import annotations

import math
import uuid
from collections import Counter
from datetime import UTC, datetime

import structlog
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_term_idf import JobTermIdf
from app.models.normalized_job import NormalizedJob
from app.scoring.text_corpus import IdfJobText, job_tokens

log = structlog.get_logger(__name__)

BM25_K1 = 1.5
BM25_B = 0.75
DEFAULT_BATCH_SIZE = 500
INSERT_BATCH_SIZE = 5000

_IDF_JOB_COLUMNS = (
    NormalizedJob.id,
    NormalizedJob.description_text,
    NormalizedJob.description_preview,
    NormalizedJob.responsibilities,
    NormalizedJob.required_qualifications,
    NormalizedJob.preferred_qualifications,
    NormalizedJob.tech_stack,
    NormalizedJob.skills,
)


def compute_idf(term_df: int, corpus_size: int) -> float:
    if corpus_size <= 0 or term_df <= 0:
        return 0.0
    return math.log(1.0 + (corpus_size - term_df + 0.5) / (term_df + 0.5))


def _row_to_idf_job(row: tuple) -> IdfJobText:
    return IdfJobText(
        description_text=row[1],
        description_preview=row[2],
        responsibilities=list(row[3] or []),
        required_qualifications=list(row[4] or []),
        preferred_qualifications=list(row[5] or []),
        tech_stack=list(row[6] or []),
        skills=list(row[7] or []),
    )


async def _iter_idf_job_batches(
    db: AsyncSession,
    *,
    batch_size: int,
) -> tuple[int, Counter[str], int]:
    document_frequencies: Counter[str] = Counter()
    corpus_size = 0
    scanned = 0
    last_id: uuid.UUID | None = None

    while True:
        stmt = (
            select(*_IDF_JOB_COLUMNS)
            .where(
                NormalizedJob.is_active.is_(True),
                NormalizedJob.processing_state == "success",
            )
            .order_by(NormalizedJob.id)
            .limit(batch_size)
        )
        if last_id is not None:
            stmt = stmt.where(NormalizedJob.id > last_id)

        rows = (await db.execute(stmt)).all()
        if not rows:
            break

        for row in rows:
            scanned += 1
            tokens = job_tokens(_row_to_idf_job(row))
            if not tokens:
                continue
            corpus_size += 1
            document_frequencies.update(set(tokens))

        last_id = rows[-1][0]
        log.info(
            "idf_corpus_batch_scanned",
            batch_jobs=len(rows),
            scanned=scanned,
            indexed=corpus_size,
            unique_terms=len(document_frequencies),
        )

    return scanned, document_frequencies, corpus_size


async def build_idf_corpus(db: AsyncSession, *, batch_size: int = DEFAULT_BATCH_SIZE) -> dict[str, int]:
    scanned, document_frequencies, corpus_size = await _iter_idf_job_batches(
        db,
        batch_size=batch_size,
    )
    if scanned == 0:
        log.warning("idf_corpus_empty")
        return {"jobs": 0, "terms": 0, "scanned": 0}

    if corpus_size == 0:
        log.warning("idf_corpus_no_tokens", scanned=scanned)
        return {"jobs": 0, "terms": 0, "scanned": scanned}

    now = datetime.now(UTC)
    await db.execute(delete(JobTermIdf))

    terms = list(document_frequencies.items())
    for offset in range(0, len(terms), INSERT_BATCH_SIZE):
        chunk = terms[offset : offset + INSERT_BATCH_SIZE]
        db.add_all(
            [
                JobTermIdf(
                    term=term,
                    document_frequency=df,
                    idf=compute_idf(df, corpus_size),
                    corpus_size=corpus_size,
                    updated_at=now,
                )
                for term, df in chunk
            ]
        )
        await db.flush()

    await db.commit()
    log.info("idf_corpus_built", scanned=scanned, jobs=corpus_size, terms=len(terms))
    return {"scanned": scanned, "jobs": corpus_size, "terms": len(terms)}
