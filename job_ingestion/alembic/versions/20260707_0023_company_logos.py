"""add company logo fields

Revision ID: 20260707_0023
Revises: 20260705_0022
Create Date: 2026-07-07 22:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260707_0023"
down_revision: str = "20260705_0022"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("companies", sa.Column("logo_url", sa.String(length=512), nullable=True))
    op.add_column("companies", sa.Column("logo_domain", sa.String(length=255), nullable=True))
    op.add_column(
        "companies",
        sa.Column("logo_status", sa.String(length=16), nullable=False, server_default="pending"),
    )
    op.add_column("companies", sa.Column("logo_fetched_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("companies", "logo_fetched_at")
    op.drop_column("companies", "logo_status")
    op.drop_column("companies", "logo_domain")
    op.drop_column("companies", "logo_url")
