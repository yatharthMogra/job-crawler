"""qualification fit display calibration

Revision ID: 20260711_0026
Revises: 20260711_0025
Create Date: 2026-07-11 15:30:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260711_0026"
down_revision: str = "20260711_0025"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "qualification_fit_calibration",
        sa.Column("id", sa.Integer(), primary_key=True, server_default="1"),
        sa.Column("raw_p5", sa.Float(), nullable=False, server_default="0"),
        sa.Column("raw_p95", sa.Float(), nullable=False, server_default="1"),
        sa.Column("sample_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.execute(
        "INSERT INTO qualification_fit_calibration (id, raw_p5, raw_p95, sample_size) "
        "VALUES (1, 0, 1, 0) ON CONFLICT DO NOTHING"
    )


def downgrade() -> None:
    op.drop_table("qualification_fit_calibration")
