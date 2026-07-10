"""Add resume content embeddings for ATS fit scoring

Revision ID: 20260710_0006
Revises: 20260706_0005
Create Date: 2026-07-10 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260710_0006"
down_revision: str = "20260706_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "candidate_resumes",
        sa.Column("content_embedding", postgresql.ARRAY(sa.Float()), nullable=True),
    )
    op.add_column(
        "candidate_resumes",
        sa.Column("content_embedding_model", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "candidate_resumes",
        sa.Column("content_embedding_computed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("candidate_resumes", "content_embedding_computed_at")
    op.drop_column("candidate_resumes", "content_embedding_model")
    op.drop_column("candidate_resumes", "content_embedding")
