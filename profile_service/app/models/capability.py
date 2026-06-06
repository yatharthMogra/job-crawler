from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate


class CandidateCapability(Base):
    __tablename__ = "candidate_capabilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    profile_version: Mapped[int] = mapped_column(Integer, nullable=False)
    taxonomy_version: Mapped[str] = mapped_column(String(16), nullable=False, default="v1")
    capability_name: Mapped[str] = mapped_column(String(128), nullable=False)
    supporting_evidence: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    candidate: Mapped["Candidate"] = relationship(back_populates="capabilities")
