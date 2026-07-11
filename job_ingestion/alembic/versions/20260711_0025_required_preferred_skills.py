"""required_skills and preferred_skills on normalized_jobs and job_enrichments

Revision ID: 20260711_0025
Revises: 20260710_0024
Create Date: 2026-07-11 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260711_0025"
down_revision: str = "20260710_0024"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SKILL_COLUMNS = ("required_skills", "preferred_skills")


def upgrade() -> None:
    for table in ("normalized_jobs", "job_enrichments"):
        for column in _SKILL_COLUMNS:
            op.add_column(
                table,
                sa.Column(
                    column,
                    postgresql.ARRAY(sa.String(length=128)),
                    nullable=False,
                    server_default=sa.text("'{}'"),
                ),
            )


def downgrade() -> None:
    for table in ("normalized_jobs", "job_enrichments"):
        for column in reversed(_SKILL_COLUMNS):
            op.drop_column(table, column)
