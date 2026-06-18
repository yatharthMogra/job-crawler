"""add job_country to normalized_jobs

Revision ID: 20260612_0010
Revises: 20260611_0009
Create Date: 2026-06-12 14:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260612_0010"
down_revision: str = "20260611_0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("normalized_jobs", sa.Column("job_country", sa.String(length=2), nullable=True))
    op.create_index("idx_normalized_jobs_job_country", "normalized_jobs", ["job_country"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_normalized_jobs_job_country", table_name="normalized_jobs")
    op.drop_column("normalized_jobs", "job_country")
