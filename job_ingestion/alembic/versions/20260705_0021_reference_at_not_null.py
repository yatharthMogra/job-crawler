"""set reference_at NOT NULL after backfill

Revision ID: 20260705_0021
Revises: 20260705_0020
Create Date: 2026-07-05 18:01:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260705_0021"
down_revision: str = "20260705_0020"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "normalized_jobs",
        "reference_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "normalized_jobs",
        "reference_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
    )
