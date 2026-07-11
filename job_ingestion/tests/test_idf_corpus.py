from __future__ import annotations

from collections import Counter

from app.ingestion.idf_corpus import compute_idf
from app.scoring.text_corpus import IdfJobText, job_tokens


def test_job_tokens_from_idf_job_text() -> None:
    job = IdfJobText(
        description_text="Python data pipelines and Spark",
        description_preview=None,
        responsibilities=["Build ETL systems"],
        required_qualifications=["BS in CS"],
        preferred_qualifications=[],
        tech_stack=["Python", "Spark"],
        skills=["Airflow"],
    )
    tokens = job_tokens(job)
    assert "python" in tokens
    assert "spark" in tokens


def test_compute_idf_increases_for_rarer_terms() -> None:
    common = compute_idf(term_df=1000, corpus_size=2000)
    rare = compute_idf(term_df=10, corpus_size=2000)
    assert rare > common


def test_idf_job_text_fields_only() -> None:
    job = IdfJobText(
        description_text="test",
        description_preview=None,
        responsibilities=[],
        required_qualifications=[],
        preferred_qualifications=[],
        tech_stack=[],
        skills=[],
    )
    assert job_tokens(job) == ["test"]
