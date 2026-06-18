from __future__ import annotations

from app.ingestion.constants_taxonomy import ROLE_INTENTS, coerce_role_intent
from app.ingestion.extractor.llm import (
    ENRICHMENT_SYSTEM_PROMPT,
    BatchJobEnrichment,
    JobEnrichment,
)


def test_role_intent_prompt_in_system_prompt() -> None:
    assert "role_intent:" in ENRICHMENT_SYSTEM_PROMPT
    assert "requires_clearance:" in ENRICHMENT_SYSTEM_PROMPT
    assert "clearance sponsorship available" in ENRICHMENT_SYSTEM_PROMPT


def test_coerce_role_intent_valid() -> None:
    assert coerce_role_intent("engineer") == "engineer"
    assert coerce_role_intent("EDUCATOR") == "educator"


def test_coerce_role_intent_invalid_defaults_other() -> None:
    assert coerce_role_intent("not_a_real_intent") == "other"
    assert coerce_role_intent(None) == "other"


def test_batch_enrichment_coerces_role_intent() -> None:
    parsed = BatchJobEnrichment.model_validate(
        {
            "job_id": "abc",
            "is_internship": False,
            "is_new_grad": False,
            "role_intent": "bogus",
        }
    )
    assert parsed.role_intent == "other"


def test_batch_enrichment_educator_intent() -> None:
    parsed = BatchJobEnrichment.model_validate(
        {
            "job_id": "abc",
            "is_internship": False,
            "is_new_grad": False,
            "role_intent": "educator",
            "normalized_roles": ["ML_ENGINEER"],
        }
    )
    assert parsed.role_intent == "educator"


def test_requires_clearance_defaults_false() -> None:
    parsed = BatchJobEnrichment.model_validate(
        {
            "job_id": "abc",
            "is_internship": False,
            "is_new_grad": False,
        }
    )
    assert parsed.requires_clearance is False


def test_requires_clearance_coerces_true() -> None:
    parsed = BatchJobEnrichment.model_validate(
        {
            "job_id": "abc",
            "is_internship": False,
            "is_new_grad": False,
            "requires_clearance": "true",
        }
    )
    assert parsed.requires_clearance is True


def test_job_enrichment_includes_new_fields() -> None:
    parsed = JobEnrichment.model_validate(
        {
            "is_internship": False,
            "is_new_grad": False,
            "sponsorship_status": "unclear",
            "sponsorship_confidence": "low",
            "remote_type": "unclear",
            "requires_clearance": True,
            "role_intent": "engineer",
        }
    )
    assert parsed.requires_clearance is True
    assert parsed.role_intent == "engineer"


def test_all_role_intents_are_valid_in_taxonomy() -> None:
    for intent in ROLE_INTENTS:
        assert coerce_role_intent(intent) == intent
