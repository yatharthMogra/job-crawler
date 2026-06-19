"""H-1B dataset tables."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260613_0001"
down_revision = "20260613_0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "soc_to_pool_mapping",
        sa.Column("soc_code", sa.String(length=10), nullable=False),
        sa.Column("soc_title", sa.Text(), nullable=False),
        sa.Column("pool_family", sa.String(length=50), nullable=False),
        sa.Column("domain_hint", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("soc_code"),
    )

    op.create_table(
        "lca_raw",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("employer_name_raw", sa.Text(), nullable=False),
        sa.Column("soc_code", sa.String(length=10), nullable=True),
        sa.Column("soc_title", sa.Text(), nullable=True),
        sa.Column("job_title", sa.Text(), nullable=True),
        sa.Column("wage_from", sa.Numeric(), nullable=True),
        sa.Column("wage_unit", sa.String(length=20), nullable=True),
        sa.Column("worksite_state", sa.String(length=2), nullable=True),
        sa.Column("worksite_city", sa.Text(), nullable=True),
        sa.Column("case_status", sa.String(length=30), nullable=True),
        sa.Column("visa_class", sa.String(length=10), nullable=True),
        sa.Column("received_date", sa.Date(), nullable=True),
        sa.Column("decision_date", sa.Date(), nullable=True),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("source_file", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "employer_name_raw",
            "soc_code",
            "received_date",
            "fiscal_year",
            name="uq_lca_raw_dedup",
        ),
    )
    op.create_index("ix_lca_raw_fiscal_year", "lca_raw", ["fiscal_year"], unique=False)
    op.create_index("ix_lca_raw_employer_name_raw", "lca_raw", ["employer_name_raw"], unique=False)

    op.create_table(
        "uscis_raw",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("employer_name_raw", sa.Text(), nullable=False),
        sa.Column("naics_code", sa.String(length=10), nullable=True),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("initial_approvals", sa.Integer(), server_default="0", nullable=False),
        sa.Column("initial_denials", sa.Integer(), server_default="0", nullable=False),
        sa.Column("continuing_approvals", sa.Integer(), server_default="0", nullable=False),
        sa.Column("continuing_denials", sa.Integer(), server_default="0", nullable=False),
        sa.Column("source_file", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "employer_name_raw",
            "fiscal_year",
            "naics_code",
            name="uq_uscis_raw_dedup",
        ),
    )
    op.create_index("ix_uscis_raw_fiscal_year", "uscis_raw", ["fiscal_year"], unique=False)

    op.create_table(
        "h1b_employers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employer_name_norm", sa.Text(), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("match_method", sa.String(length=20), nullable=True),
        sa.Column("match_confidence", sa.Numeric(precision=4, scale=3), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("employer_name_norm"),
    )
    op.create_index("ix_h1b_employers_company_id", "h1b_employers", ["company_id"], unique=False)

    op.create_table(
        "h1b_employer_aliases",
        sa.Column("employer_name_raw", sa.Text(), nullable=False),
        sa.Column("employer_name_norm", sa.Text(), nullable=False),
        sa.Column("first_seen_year", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["employer_name_norm"], ["h1b_employers.employer_name_norm"]),
        sa.PrimaryKeyConstraint("employer_name_raw"),
    )

    op.create_table(
        "h1b_lca_stats",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employer_name_norm", sa.Text(), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("soc_code", sa.String(length=10), nullable=True),
        sa.Column("pool_family", sa.String(length=50), nullable=True),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("lca_certified", sa.Integer(), server_default="0", nullable=False),
        sa.Column("lca_denied", sa.Integer(), server_default="0", nullable=False),
        sa.Column("lca_withdrawn", sa.Integer(), server_default="0", nullable=False),
        sa.Column("avg_wage_annual", sa.Numeric(), nullable=True),
        sa.Column("primary_state", sa.String(length=2), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["employer_name_norm"], ["h1b_employers.employer_name_norm"]),
        sa.ForeignKeyConstraint(["soc_code"], ["soc_to_pool_mapping.soc_code"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "employer_name_norm",
            "soc_code",
            "fiscal_year",
            name="uq_h1b_lca_stats",
        ),
    )
    op.create_index(
        "ix_h1b_lca_stats_company_pool",
        "h1b_lca_stats",
        ["company_id", "pool_family", "fiscal_year"],
        unique=False,
    )

    op.create_table(
        "h1b_uscis_stats",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employer_name_norm", sa.Text(), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("initial_approvals", sa.Integer(), server_default="0", nullable=False),
        sa.Column("initial_denials", sa.Integer(), server_default="0", nullable=False),
        sa.Column("continuing_approvals", sa.Integer(), server_default="0", nullable=False),
        sa.Column("continuing_denials", sa.Integer(), server_default="0", nullable=False),
        sa.Column("approval_rate", sa.Numeric(precision=5, scale=4), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["employer_name_norm"], ["h1b_employers.employer_name_norm"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "employer_name_norm",
            "fiscal_year",
            name="uq_h1b_uscis_stats",
        ),
    )
    op.create_index(
        "ix_h1b_uscis_stats_company_year",
        "h1b_uscis_stats",
        ["company_id", "fiscal_year"],
        unique=False,
    )

    op.create_table(
        "h1b_company_pool_summary",
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("pool_family", sa.String(length=50), nullable=False),
        sa.Column("years_covered", postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column("latest_year", sa.Integer(), nullable=True),
        sa.Column("total_lca_3yr", sa.Integer(), nullable=True),
        sa.Column("total_h1b_3yr", sa.Integer(), nullable=True),
        sa.Column("approval_rate_3yr", sa.Numeric(precision=5, scale=4), nullable=True),
        sa.Column("is_top_sponsor", sa.Boolean(), nullable=True),
        sa.Column(
            "last_updated",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("company_id", "pool_family"),
    )


def downgrade() -> None:
    op.drop_table("h1b_company_pool_summary")
    op.drop_table("h1b_uscis_stats")
    op.drop_table("h1b_lca_stats")
    op.drop_table("h1b_employer_aliases")
    op.drop_table("h1b_employers")
    op.drop_table("uscis_raw")
    op.drop_table("lca_raw")
    op.drop_table("soc_to_pool_mapping")
