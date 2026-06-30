"""experience_tier column

Revision ID: 20260627_0017
Revises: 20260623_0016
Create Date: 2026-06-27 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260627_0017"
down_revision: str = "20260623_0016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "normalized_jobs",
        sa.Column("experience_tier", sa.String(length=32), nullable=False, server_default="UNKNOWN"),
    )
    op.add_column(
        "job_enrichments",
        sa.Column("experience_tier", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "job_archive",
        sa.Column("experience_tier", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("job_archive", "experience_tier")
    op.drop_column("job_enrichments", "experience_tier")
    op.drop_column("normalized_jobs", "experience_tier")
