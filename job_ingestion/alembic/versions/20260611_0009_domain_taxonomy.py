"""domain taxonomy columns

Revision ID: 20260611_0009
Revises: 20260610_0008
Create Date: 2026-06-11 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260611_0009"
down_revision: str = "20260610_0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("normalized_jobs", sa.Column("job_domain", sa.String(length=64), nullable=True))
    op.add_column(
        "normalized_jobs",
        sa.Column("job_secondary_domain", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_normalized_jobs_job_domain", "normalized_jobs", ["job_domain"])

    op.add_column("job_archive", sa.Column("job_domain", sa.String(length=64), nullable=True))
    op.add_column(
        "job_archive",
        sa.Column("job_secondary_domain", sa.String(length=64), nullable=True),
    )

    op.add_column(
        "candidate_profiles",
        sa.Column("primary_domain", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "candidate_profiles",
        sa.Column("secondary_domain", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("candidate_profiles", "secondary_domain")
    op.drop_column("candidate_profiles", "primary_domain")
    op.drop_column("job_archive", "job_secondary_domain")
    op.drop_column("job_archive", "job_domain")
    op.drop_index("ix_normalized_jobs_job_domain", table_name="normalized_jobs")
    op.drop_column("normalized_jobs", "job_secondary_domain")
    op.drop_column("normalized_jobs", "job_domain")
