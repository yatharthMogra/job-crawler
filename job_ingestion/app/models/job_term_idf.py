from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobTermIdf(Base):
    __tablename__ = "job_term_idf"

    term: Mapped[str] = mapped_column(String(256), primary_key=True)
    document_frequency: Mapped[int] = mapped_column(Integer, nullable=False)
    idf: Mapped[float] = mapped_column(Float, nullable=False)
    corpus_size: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class EmbeddingCalibration(Base):
    __tablename__ = "embedding_calibration"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    min_similarity: Mapped[float] = mapped_column(Float, nullable=False, default=0.3)
    max_similarity: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False, default="all-MiniLM-L6-v2")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class QualificationFitCalibration(Base):
    __tablename__ = "qualification_fit_calibration"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    raw_p5: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    raw_p95: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
