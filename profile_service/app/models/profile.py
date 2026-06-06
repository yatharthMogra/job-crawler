from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.patch import CandidatePatch


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    __table_args__ = (
        UniqueConstraint("candidate_id", "version", name="uq_candidate_profiles_candidate_version"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    schema_version: Mapped[str] = mapped_column(String(16), nullable=False, default="v1")
    constraints: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    preferences: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    skills: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    education: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    patch_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidate_patches.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    candidate: Mapped["Candidate"] = relationship(back_populates="profiles")
    patch: Mapped[Optional["CandidatePatch"]] = relationship(
        back_populates="created_profile", foreign_keys=[patch_id]
    )
