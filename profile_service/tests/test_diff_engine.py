import uuid

import pytest

from app.pipeline.llm_parser import ExtractedExperience, LLMExtractionOutput, ExtractedSkills
from app.pipeline.diff_engine import compute_proposed_operations
from app.utils.text_utils import (
    find_experience_merge_candidate,
    is_garbage_text,
    normalize_skill,
)


class TestTextUtils:
    def test_normalize_skill_aliases(self) -> None:
        assert normalize_skill("js") == "JavaScript"
        assert normalize_skill("postgres") == "PostgreSQL"
        assert normalize_skill("k8s") == "Kubernetes"

    def test_is_garbage_text(self) -> None:
        assert is_garbage_text("") is True
        assert is_garbage_text("Hello world " * 20) is False


class TestDiffEngine:
    def test_adds_new_skills(self) -> None:
        extracted = LLMExtractionOutput(
            skills=ExtractedSkills(languages=["js", "Python"], frameworks=["FastAPI"])
        )
        ops = compute_proposed_operations(extracted, None, [])
        skill_ops = [op for op in ops if op["op"] == "ADD_SKILL"]
        assert {"category": "languages", "value": "JavaScript"} in [
            {"category": op["category"], "value": op["value"]} for op in skill_ops
        ]
        assert all("id" in op for op in ops)

    def test_experience_merge_adds_update_ops(self) -> None:
        from app.models.evidence import CandidateEvidence

        evidence = CandidateEvidence(
            id=uuid.uuid4(),
            candidate_id=uuid.uuid4(),
            source_resume_id=uuid.uuid4(),
            evidence_type="experience",
            is_active=True,
            normalized_data={
                "title": "Software Developer",
                "company": "Walmart Inc",
                "duration_months": 22,
                "domains": [],
                "evidence_keywords": [],
            },
        )
        extracted = LLMExtractionOutput(
            experiences=[
                ExtractedExperience(
                    title="Software Developer 2",
                    company="Walmart",
                    duration_months=24,
                    domains=["Retail Tech"],
                    evidence_keywords=["Java"],
                )
            ]
        )
        merge = find_experience_merge_candidate(extracted.experiences[0], [evidence])
        assert merge is not None
        ops = compute_proposed_operations(extracted, None, [evidence])
        update_ops = [op for op in ops if op["op"] == "UPDATE_EXPERIENCE"]
        assert update_ops
