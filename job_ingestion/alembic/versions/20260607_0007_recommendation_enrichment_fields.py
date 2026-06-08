"""recommendation enrichment fields

Revision ID: 20260607_0007
Revises: 20260528_0006
Create Date: 2026-06-07 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260607_0007"
down_revision: str = "20260528_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_RECOMMENDATION_COLUMNS = [
    ("normalized_roles", postgresql.ARRAY(sa.String(64)), "'{}'::varchar[]"),
    ("job_capabilities", postgresql.ARRAY(sa.String(128)), "'{}'::varchar[]"),
    ("application_effort", sa.String(16), None),
    ("retrieval_pools", postgresql.ARRAY(sa.String(128)), "'{}'::varchar[]"),
    ("salary_min", sa.Integer(), None),
    ("salary_max", sa.Integer(), None),
    ("opportunity_score", sa.Float(), None),
    ("opportunity_score_computed_at", sa.DateTime(timezone=True), None),
]


def _add_columns(table_name: str) -> None:
    for column_name, column_type, server_default in _RECOMMENDATION_COLUMNS:
        kwargs: dict = {"nullable": True}
        if server_default is not None:
            kwargs["server_default"] = sa.text(server_default)
        op.add_column(table_name, sa.Column(column_name, column_type, **kwargs))
        if server_default is not None:
            op.alter_column(table_name, column_name, server_default=None)


def _drop_columns(table_name: str) -> None:
    for column_name, _, _ in reversed(_RECOMMENDATION_COLUMNS):
        op.drop_column(table_name, column_name)


def upgrade() -> None:
    _add_columns("job_enrichments")
    _add_columns("normalized_jobs")

    op.create_index(
        "ix_job_enrichments_retrieval_pools_gin",
        "job_enrichments",
        ["retrieval_pools"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_job_enrichments_normalized_roles_gin",
        "job_enrichments",
        ["normalized_roles"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_job_enrichments_job_capabilities_gin",
        "job_enrichments",
        ["job_capabilities"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_normalized_jobs_retrieval_pools_gin",
        "normalized_jobs",
        ["retrieval_pools"],
        unique=False,
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("ix_normalized_jobs_retrieval_pools_gin", table_name="normalized_jobs")
    op.drop_index("ix_job_enrichments_job_capabilities_gin", table_name="job_enrichments")
    op.drop_index("ix_job_enrichments_normalized_roles_gin", table_name="job_enrichments")
    op.drop_index("ix_job_enrichments_retrieval_pools_gin", table_name="job_enrichments")
    _drop_columns("normalized_jobs")
    _drop_columns("job_enrichments")
