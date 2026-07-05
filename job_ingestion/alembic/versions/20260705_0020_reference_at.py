"""add reference_at to normalized_jobs

Revision ID: 20260705_0020
Revises: 20260705_0019
Create Date: 2026-07-05 18:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260705_0020"
down_revision: str = "20260705_0019"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "normalized_jobs",
        sa.Column("reference_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_normalized_jobs_reference_at",
        "normalized_jobs",
        ["reference_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_normalized_jobs_reference_at", table_name="normalized_jobs")
    op.drop_column("normalized_jobs", "reference_at")
