"""jd section fields on normalized jobs and job enrichments

Revision ID: 20260621_0014
Revises: 20260619_0013
Create Date: 2026-06-21 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260621_0014"
down_revision: str = "20260619_0013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SECTION_COLUMNS = (
    "responsibilities",
    "required_qualifications",
    "preferred_qualifications",
    "benefits",
)


def upgrade() -> None:
    for table in ("normalized_jobs", "job_enrichments"):
        for column in _SECTION_COLUMNS:
            op.add_column(
                table,
                sa.Column(
                    column,
                    postgresql.ARRAY(sa.String(length=512)),
                    nullable=False,
                    server_default=sa.text("'{}'"),
                ),
            )


def downgrade() -> None:
    for table in ("normalized_jobs", "job_enrichments"):
        for column in reversed(_SECTION_COLUMNS):
            op.drop_column(table, column)
