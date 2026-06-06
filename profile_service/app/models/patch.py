from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.profile import CandidateProfile
    from app.models.resume import CandidateResume


class CandidatePatch(Base):
    __tablename__ = "candidate_patches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidate_resumes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    profile_version_before: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    profile_version_after: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    proposed_operations: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    approved_operations: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    rejected_operations: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    committed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    candidate: Mapped["Candidate"] = relationship(back_populates="patches")
    source_resume: Mapped["CandidateResume"] = relationship(back_populates="patches")
    created_profile: Mapped[Optional["CandidateProfile"]] = relationship(
        back_populates="patch", foreign_keys="CandidateProfile.patch_id"
    )
