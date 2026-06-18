"""clearance and role_intent columns

Revision ID: 20260613_0011
Revises: 20260612_0010
Create Date: 2026-06-13 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260613_0011"
down_revision: str = "20260612_0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "normalized_jobs",
        sa.Column("requires_clearance", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "normalized_jobs",
        sa.Column("role_intent", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_normalized_jobs_role_intent", "normalized_jobs", ["role_intent"])

    op.add_column(
        "job_archive",
        sa.Column("requires_clearance", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "job_archive",
        sa.Column("role_intent", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("job_archive", "role_intent")
    op.drop_column("job_archive", "requires_clearance")
    op.drop_index("ix_normalized_jobs_role_intent", table_name="normalized_jobs")
    op.drop_column("normalized_jobs", "role_intent")
    op.drop_column("normalized_jobs", "requires_clearance")
