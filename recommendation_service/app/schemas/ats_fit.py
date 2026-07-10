from __future__ import annotations

from pydantic import BaseModel, Field


class AtsFitSignalsOut(BaseModel):
    bm25: float | None = None
    semantic: float | None = None
    structural: float | None = None
    title: float | None = None
    experience: float | None = None
    education: float | None = None


class AtsFitOut(BaseModel):
    ats_fit_score: int | None = None
    pool_percentile: int | None = None
    pool_percentile_label: str | None = None
    signals: AtsFitSignalsOut = Field(default_factory=AtsFitSignalsOut)
    unavailable_reason: str | None = None
