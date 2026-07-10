"""ATS fit score infrastructure: IDF corpus, embeddings, pool percentile cutoffs

Revision ID: 20260710_0024
Revises: 20260707_0023
Create Date: 2026-07-10 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260710_0024"
down_revision: str = "20260707_0023"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "job_term_idf",
        sa.Column("term", sa.String(length=256), primary_key=True),
        sa.Column("document_frequency", sa.Integer(), nullable=False),
        sa.Column("idf", sa.Float(), nullable=False),
        sa.Column("corpus_size", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        "embedding_calibration",
        sa.Column("id", sa.Integer(), primary_key=True, server_default="1"),
        sa.Column("min_similarity", sa.Float(), nullable=False, server_default="0.3"),
        sa.Column("max_similarity", sa.Float(), nullable=False, server_default="0.85"),
        sa.Column("model_name", sa.String(length=128), nullable=False, server_default="all-MiniLM-L6-v2"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.execute(
        "INSERT INTO embedding_calibration (id, min_similarity, max_similarity, model_name) "
        "VALUES (1, 0.3, 0.85, 'all-MiniLM-L6-v2') ON CONFLICT DO NOTHING"
    )
    op.add_column(
        "normalized_jobs",
        sa.Column("content_embedding", postgresql.ARRAY(sa.Float()), nullable=True),
    )
    op.add_column(
        "normalized_jobs",
        sa.Column("content_embedding_model", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "normalized_jobs",
        sa.Column(
            "pool_percentile_cutoffs",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("normalized_jobs", "pool_percentile_cutoffs")
    op.drop_column("normalized_jobs", "content_embedding_model")
    op.drop_column("normalized_jobs", "content_embedding")
    op.drop_table("embedding_calibration")
    op.drop_table("job_term_idf")
