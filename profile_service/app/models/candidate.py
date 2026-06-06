from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    resumes: Mapped[list["CandidateResume"]] = relationship(back_populates="candidate")
    evidence: Mapped[list["CandidateEvidence"]] = relationship(back_populates="candidate")
    profiles: Mapped[list["CandidateProfile"]] = relationship(back_populates="candidate")
    patches: Mapped[list["CandidatePatch"]] = relationship(back_populates="candidate")
    capabilities: Mapped[list["CandidateCapability"]] = relationship(back_populates="candidate")
