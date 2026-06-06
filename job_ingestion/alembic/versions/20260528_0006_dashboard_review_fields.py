"""dashboard review workflow fields

Revision ID: 20260528_0006
Revises: 20260527_0005
Create Date: 2026-05-28 12:03:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260528_0006"
down_revision: str = "20260527_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "companies",
        sa.Column("requires_review", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column("companies", sa.Column("flagged_for_review_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("companies", sa.Column("last_failure_at", sa.DateTime(timezone=True), nullable=True))
    op.alter_column("companies", "requires_review", server_default=None)

    op.add_column("normalized_jobs", sa.Column("last_manual_review_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("normalized_jobs", sa.Column("last_review_comment", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("normalized_jobs", "last_review_comment")
    op.drop_column("normalized_jobs", "last_manual_review_at")

    op.drop_column("companies", "last_failure_at")
    op.drop_column("companies", "flagged_for_review_at")
    op.drop_column("companies", "requires_review")
