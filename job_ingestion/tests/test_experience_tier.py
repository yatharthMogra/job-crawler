from __future__ import annotations

from app.ingestion.extractor.experience_tier import (
    EXPERIENCE_TIER_ORDER,
    apply_experience_tier_consistency,
    normalize_experience_tier,
    tier_index,
    tiers_above_ceiling,
)


def test_normalize_experience_tier_canonical() -> None:
    assert normalize_experience_tier("MID") == "MID"
    assert normalize_experience_tier("above_senior") == "ABOVE_SENIOR"


def test_normalize_experience_tier_invalid() -> None:
    assert normalize_experience_tier("STAFF") == "ABOVE_SENIOR"
    assert normalize_experience_tier("not-a-tier") == "UNKNOWN"
    assert normalize_experience_tier(None) == "UNKNOWN"


def test_tier_index() -> None:
    assert tier_index("INTERN") == 0
    assert tier_index("ABOVE_SENIOR") == len(EXPERIENCE_TIER_ORDER) - 1
    assert tier_index("UNKNOWN") is None


def test_tiers_above_ceiling() -> None:
    hidden = tiers_above_ceiling("SENIOR")
    assert hidden == frozenset({"ABOVE_SENIOR"})
    assert tiers_above_ceiling("ABOVE_SENIOR") == frozenset()


def test_apply_experience_tier_consistency_internship() -> None:
    assert apply_experience_tier_consistency("MID", True, False) == "INTERN"
    assert apply_experience_tier_consistency("MID", False, True) == "NEW_GRAD"


def test_finalize_enrichment_sets_experience_tier() -> None:
    from app.ingestion.extractor.llm import JobEnrichment, finalize_enrichment

    enrichment = JobEnrichment(
        seniority="MID",
        experience_tier="MID",
        is_internship=False,
        is_new_grad=False,
        sponsorship_status="unclear",
        sponsorship_confidence="low",
        remote_type="unclear",
    )
    finalized = finalize_enrichment(
        enrichment,
        title="Software Engineering Intern",
        employment_type="Internship",
    )
    assert finalized.experience_tier == "INTERN"
    assert finalized.seniority == "INTERN"
