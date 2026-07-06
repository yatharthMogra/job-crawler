"""Add candidate auth fields and auth_challenges table."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260706_0004"
down_revision = "20260616_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "candidates",
        sa.Column("signup_method", sa.String(length=16), nullable=False, server_default="email"),
    )
    op.add_column(
        "candidates",
        sa.Column("password_hash", sa.String(length=255), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE candidates SET signup_method = 'google' WHERE google_sub IS NOT NULL"
        )
    )

    op.create_table(
        "auth_challenges",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("purpose", sa.String(length=16), nullable=False),
        sa.Column("challenge_token", sa.String(length=64), nullable=False),
        sa.Column("code_hash", sa.String(length=255), nullable=False),
        sa.Column("pending_name", sa.String(length=255), nullable=True),
        sa.Column("pending_password_hash", sa.String(length=255), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auth_challenges_email", "auth_challenges", ["email"])
    op.create_index(
        "ix_auth_challenges_challenge_token",
        "auth_challenges",
        ["challenge_token"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_auth_challenges_challenge_token", table_name="auth_challenges")
    op.drop_index("ix_auth_challenges_email", table_name="auth_challenges")
    op.drop_table("auth_challenges")
    op.drop_column("candidates", "password_hash")
    op.drop_column("candidates", "signup_method")
