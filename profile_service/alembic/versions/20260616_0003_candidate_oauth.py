"""Add OAuth fields to candidates."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260616_0003"
down_revision = "20260607_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("candidates", sa.Column("google_sub", sa.String(length=255), nullable=True))
    op.add_column("candidates", sa.Column("avatar_url", sa.String(length=512), nullable=True))
    op.add_column(
        "candidates",
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_candidates_google_sub", "candidates", ["google_sub"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_candidates_google_sub", table_name="candidates")
    op.drop_column("candidates", "email_verified")
    op.drop_column("candidates", "avatar_url")
    op.drop_column("candidates", "google_sub")
