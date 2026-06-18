from __future__ import annotations

from app.ingestion.dedup import build_dedup_fingerprint


def test_build_dedup_fingerprint_normalizes_company_and_title() -> None:
    fp = build_dedup_fingerprint("Acme Inc.", "Senior Backend Engineer", "San Francisco, CA")
    assert fp == "acme|senior backend engineer|san francisco"


def test_build_dedup_fingerprint_matches_greenhouse_style() -> None:
    gh = build_dedup_fingerprint("Figma", "Backend Engineer, Data", "New York, NY")
    waas = build_dedup_fingerprint("Figma", "Backend Engineer Data", "New York, NY")
    assert gh == waas


def test_build_dedup_fingerprint_handles_remote() -> None:
    fp = build_dedup_fingerprint("Startup", "Software Engineer", "Remote")
    assert fp.endswith("|remote")
