"""Add plan tier fields to candidates."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260706_0005"
down_revision = "20260706_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "candidates",
        sa.Column("plan_tier", sa.String(length=16), nullable=False, server_default="free"),
    )
    op.add_column(
        "candidates",
        sa.Column("plan_expires_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("candidates", "plan_expires_at")
    op.drop_column("candidates", "plan_tier")
