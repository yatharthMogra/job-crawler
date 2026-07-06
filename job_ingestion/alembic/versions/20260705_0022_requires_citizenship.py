"""add requires_citizenship to normalized_jobs and job_archive

Revision ID: 20260705_0022
Revises: 20260705_0021
Create Date: 2026-07-05 20:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260705_0022"
down_revision: str = "20260705_0021"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "normalized_jobs",
        sa.Column("requires_citizenship", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "job_archive",
        sa.Column("requires_citizenship", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("job_archive", "requires_citizenship")
    op.drop_column("normalized_jobs", "requires_citizenship")
