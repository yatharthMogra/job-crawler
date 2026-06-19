"""fetch_tier on companies and schedule_metadata on pipeline_runs

Revision ID: 20260619_0013
Revises: 20260614_0012
Create Date: 2026-06-19 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260619_0013"
down_revision: str = "20260614_0012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "companies",
        sa.Column("fetch_tier", sa.Integer(), nullable=False, server_default="2"),
    )
    op.create_check_constraint(
        "ck_companies_fetch_tier",
        "companies",
        "fetch_tier IN (1, 2, 3)",
    )
    op.add_column(
        "pipeline_runs",
        sa.Column("schedule_metadata", sa.dialects.postgresql.JSONB(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("pipeline_runs", "schedule_metadata")
    op.drop_constraint("ck_companies_fetch_tier", "companies", type_="check")
    op.drop_column("companies", "fetch_tier")
