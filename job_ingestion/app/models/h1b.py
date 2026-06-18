from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SocToPoolMapping(Base):
    __tablename__ = "soc_to_pool_mapping"

    soc_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    soc_title: Mapped[str] = mapped_column(Text, nullable=False)
    pool_family: Mapped[str] = mapped_column(String(50), nullable=False)
    domain_hint: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)


class LcaRaw(Base):
    __tablename__ = "lca_raw"
    __table_args__ = (
        UniqueConstraint(
            "employer_name_raw",
            "soc_code",
            "received_date",
            "fiscal_year",
            name="uq_lca_raw_dedup",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    employer_name_raw: Mapped[str] = mapped_column(Text, nullable=False)
    soc_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    soc_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    wage_from: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    wage_unit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    worksite_state: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    worksite_city: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    case_status: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    visa_class: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    received_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    decision_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    source_file: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class UscisRaw(Base):
    __tablename__ = "uscis_raw"
    __table_args__ = (
        UniqueConstraint(
            "employer_name_raw",
            "fiscal_year",
            "naics_code",
            name="uq_uscis_raw_dedup",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    employer_name_raw: Mapped[str] = mapped_column(Text, nullable=False)
    naics_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_approvals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    initial_denials: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    continuing_approvals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    continuing_denials: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    source_file: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class H1bEmployer(Base):
    __tablename__ = "h1b_employers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employer_name_norm: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True
    )
    match_method: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    match_confidence: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 3), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class H1bEmployerAlias(Base):
    __tablename__ = "h1b_employer_aliases"

    employer_name_raw: Mapped[str] = mapped_column(Text, primary_key=True)
    employer_name_norm: Mapped[str] = mapped_column(
        Text,
        ForeignKey("h1b_employers.employer_name_norm"),
        nullable=False,
    )
    first_seen_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class H1bLcaStats(Base):
    __tablename__ = "h1b_lca_stats"
    __table_args__ = (
        UniqueConstraint(
            "employer_name_norm",
            "soc_code",
            "fiscal_year",
            name="uq_h1b_lca_stats",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employer_name_norm: Mapped[str] = mapped_column(
        Text,
        ForeignKey("h1b_employers.employer_name_norm"),
        nullable=False,
    )
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True
    )
    soc_code: Mapped[Optional[str]] = mapped_column(
        String(10), ForeignKey("soc_to_pool_mapping.soc_code"), nullable=True
    )
    pool_family: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    lca_certified: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lca_denied: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lca_withdrawn: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_wage_annual: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    primary_state: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)


class H1bUscisStats(Base):
    __tablename__ = "h1b_uscis_stats"
    __table_args__ = (
        UniqueConstraint(
            "employer_name_norm",
            "fiscal_year",
            name="uq_h1b_uscis_stats",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employer_name_norm: Mapped[str] = mapped_column(
        Text,
        ForeignKey("h1b_employers.employer_name_norm"),
        nullable=False,
    )
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True
    )
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_approvals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    initial_denials: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    continuing_approvals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    continuing_denials: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    approval_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 4), nullable=True)


class H1bCompanyPoolSummary(Base):
    __tablename__ = "h1b_company_pool_summary"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id"), primary_key=True
    )
    pool_family: Mapped[str] = mapped_column(String(50), primary_key=True)
    years_covered: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False, default=list)
    latest_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_lca_3yr: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_h1b_3yr: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    approval_rate_3yr: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 4), nullable=True)
    is_top_sponsor: Mapped[Optional[bool]] = mapped_column(nullable=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
