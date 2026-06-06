"""Initial profile service schema."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260606_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "candidates",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_candidates_email", "candidates", ["email"], unique=True)

    op.create_table(
        "candidate_resumes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("file_path", sa.String(length=512), nullable=False),
        sa.Column("original_filename", sa.String(length=512), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False),
        sa.Column("extraction_method", sa.String(length=32), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("raw_text_char_count", sa.Integer(), nullable=True),
        sa.Column("extraction_status", sa.String(length=32), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("parsed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_candidate_resumes_candidate_id", "candidate_resumes", ["candidate_id"], unique=False)

    op.create_table(
        "candidate_patches",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_resume_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("profile_version_before", sa.Integer(), nullable=True),
        sa.Column("profile_version_after", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("proposed_operations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("approved_operations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("rejected_operations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("committed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_resume_id"], ["candidate_resumes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_candidate_patches_candidate_id", "candidate_patches", ["candidate_id"], unique=False)
    op.create_index(
        "ix_candidate_patches_source_resume_id", "candidate_patches", ["source_resume_id"], unique=False
    )

    op.create_table(
        "candidate_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("schema_version", sa.String(length=16), nullable=False),
        sa.Column("constraints", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("preferences", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("skills", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("education", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("patch_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["patch_id"], ["candidate_patches.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("candidate_id", "version", name="uq_candidate_profiles_candidate_version"),
    )
    op.create_index("ix_candidate_profiles_candidate_id", "candidate_profiles", ["candidate_id"], unique=False)
    op.create_index(
        "ix_candidate_profiles_one_current",
        "candidate_profiles",
        ["candidate_id"],
        unique=True,
        postgresql_where=sa.text("is_current = true"),
    )

    op.create_table(
        "candidate_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_resume_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evidence_type", sa.String(length=32), nullable=False),
        sa.Column("is_approved", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("raw_source_text", sa.Text(), nullable=True),
        sa.Column("normalized_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_resume_id"], ["candidate_resumes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_candidate_evidence_candidate_id", "candidate_evidence", ["candidate_id"], unique=False)
    op.create_index(
        "ix_candidate_evidence_source_resume_id", "candidate_evidence", ["source_resume_id"], unique=False
    )

    op.create_table(
        "candidate_capabilities",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("profile_version", sa.Integer(), nullable=False),
        sa.Column("taxonomy_version", sa.String(length=16), nullable=False),
        sa.Column("capability_name", sa.String(length=128), nullable=False),
        sa.Column("supporting_evidence", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_candidate_capabilities_candidate_id", "candidate_capabilities", ["candidate_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_candidate_capabilities_candidate_id", table_name="candidate_capabilities")
    op.drop_table("candidate_capabilities")
    op.drop_index("ix_candidate_evidence_source_resume_id", table_name="candidate_evidence")
    op.drop_index("ix_candidate_evidence_candidate_id", table_name="candidate_evidence")
    op.drop_table("candidate_evidence")
    op.drop_index("ix_candidate_profiles_one_current", table_name="candidate_profiles")
    op.drop_index("ix_candidate_profiles_candidate_id", table_name="candidate_profiles")
    op.drop_table("candidate_profiles")
    op.drop_index("ix_candidate_patches_source_resume_id", table_name="candidate_patches")
    op.drop_index("ix_candidate_patches_candidate_id", table_name="candidate_patches")
    op.drop_table("candidate_patches")
    op.drop_index("ix_candidate_resumes_candidate_id", table_name="candidate_resumes")
    op.drop_table("candidate_resumes")
    op.drop_index("ix_candidates_email", table_name="candidates")
    op.drop_table("candidates")
