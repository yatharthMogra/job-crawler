"""enrichment worker state

Revision ID: 20260703_0018
Revises: 20260627_0017
Create Date: 2026-07-03 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260703_0018"
down_revision: str = "20260627_0017"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "enrichment_worker_state",
        sa.Column("worker_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("api_calls", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column(
            "capacity_mode",
            sa.String(length=32),
            nullable=False,
            server_default=sa.text("'normal'"),
        ),
        sa.Column(
            "rate_limit_backoff_attempt",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("rate_limited_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("enrichment_worker_state")
