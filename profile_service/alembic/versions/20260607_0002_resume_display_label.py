"""Add display_label to candidate_resumes."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260607_0002"
down_revision = "20260606_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "candidate_resumes",
        sa.Column("display_label", sa.String(length=128), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("candidate_resumes", "display_label")
