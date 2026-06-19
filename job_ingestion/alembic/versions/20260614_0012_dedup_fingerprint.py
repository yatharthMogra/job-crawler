"""dedup_fingerprint column on normalized_jobs

Revision ID: 20260614_0012
Revises: 20260613_0001
Create Date: 2026-06-14 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260614_0012"
down_revision: str = "20260613_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "normalized_jobs",
        sa.Column("dedup_fingerprint", sa.String(length=200), nullable=True),
    )
    op.create_index(
        "idx_normalized_jobs_dedup_fingerprint",
        "normalized_jobs",
        ["dedup_fingerprint"],
        unique=False,
        postgresql_where=sa.text("is_active = TRUE"),
    )


def downgrade() -> None:
    op.drop_index("idx_normalized_jobs_dedup_fingerprint", table_name="normalized_jobs")
    op.drop_column("normalized_jobs", "dedup_fingerprint")
