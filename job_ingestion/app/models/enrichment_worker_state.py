from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EnrichmentWorkerState(Base):
    __tablename__ = "enrichment_worker_state"

    worker_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    api_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    capacity_mode: Mapped[str] = mapped_column(String(32), nullable=False, default="normal")
    rate_limit_backoff_attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rate_limited_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
