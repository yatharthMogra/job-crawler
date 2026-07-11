from __future__ import annotations

import argparse
import asyncio
import json
import uuid
from datetime import UTC, datetime

import structlog
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.embeddings.service import embed_text, embedding_model_name
from app.models.resume import CandidateResume
from app.utils.logging import configure_logging

log = structlog.get_logger(__name__)

DEFAULT_BATCH_SIZE = 500


async def backfill_missing_resume_embeddings(
    *,
    batch_size: int = DEFAULT_BATCH_SIZE,
    max_batches: int | None = None,
) -> dict[str, int]:
    last_uploaded_at: datetime | None = None
    last_id: uuid.UUID | None = None
    total_updated = 0
    total_skipped = 0
    batches = 0

    async with AsyncSessionLocal() as db:
        while True:
            if max_batches is not None and batches >= max_batches:
                break

            stmt = (
                select(CandidateResume)
                .where(
                    CandidateResume.content_embedding.is_(None),
                    CandidateResume.extraction_status == "success",
                    CandidateResume.raw_text.is_not(None),
                )
                .order_by(CandidateResume.uploaded_at.asc(), CandidateResume.id.asc())
                .limit(batch_size)
            )
            if last_uploaded_at is not None and last_id is not None:
                stmt = stmt.where(
                    (CandidateResume.uploaded_at > last_uploaded_at)
                    | (
                        (CandidateResume.uploaded_at == last_uploaded_at)
                        & (CandidateResume.id > last_id)
                    )
                )

            resumes = list((await db.scalars(stmt)).all())
            if not resumes:
                break

            batch_updated = 0
            batch_skipped = 0
            for resume in resumes:
                raw_text = (resume.raw_text or "").strip()
                if not raw_text:
                    batch_skipped += 1
                    continue

                embedding = embed_text(raw_text)
                if embedding is None:
                    batch_skipped += 1
                    continue

                resume.content_embedding = embedding
                resume.content_embedding_model = embedding_model_name()
                resume.content_embedding_computed_at = datetime.now(UTC)
                batch_updated += 1

            await db.commit()
            batches += 1
            total_updated += batch_updated
            total_skipped += batch_skipped
            last_uploaded_at = resumes[-1].uploaded_at
            last_id = resumes[-1].id
            log.info(
                "resume_embedding_backfill_batch",
                batch_resumes=len(resumes),
                batch_updated=batch_updated,
                batch_skipped=batch_skipped,
                total_updated=total_updated,
                last_id=str(last_id),
            )

    return {
        "updated": total_updated,
        "skipped": total_skipped,
        "batches": batches,
    }


async def _main(*, batch_size: int, max_batches: int | None) -> None:
    configure_logging()
    result = await backfill_missing_resume_embeddings(
        batch_size=batch_size,
        max_batches=max_batches,
    )
    print(json.dumps(result, ensure_ascii=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill missing resume embeddings")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--max-batches", type=int, default=None)
    args = parser.parse_args()
    asyncio.run(_main(batch_size=args.batch_size, max_batches=args.max_batches))


if __name__ == "__main__":
    main()
