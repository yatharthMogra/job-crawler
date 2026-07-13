from __future__ import annotations

from pathlib import Path

from app.ingestion.job_content_hash import compute_job_content_hash

FIXTURES = Path(__file__).parent / "fixtures" / "google_careers"


def test_html_whitespace_changes_produce_same_hash() -> None:
    job_a = {
        "id": "101",
        "title": "Software Engineer",
        "organization": "Google",
        "location": "Mountain View, CA, USA",
        "raw_html": "<p>Build <strong>systems</strong>.</p>",
    }
    job_b = {
        **job_a,
        "raw_html": "<p>Build  <strong>systems</strong>.</p>\n",
    }
    assert compute_job_content_hash(job_a, "google_careers") == compute_job_content_hash(
        job_b, "google_careers"
    )


def test_description_text_change_produces_different_hash() -> None:
    job_a = {
        "id": "101",
        "title": "Software Engineer",
        "organization": "Google",
        "location": "Mountain View, CA, USA",
        "raw_html": "<p>BS degree required.</p>",
    }
    job_b = {
        **job_a,
        "raw_html": "<p>BS degree and MBA required.</p>",
    }
    assert compute_job_content_hash(job_a, "google_careers") != compute_job_content_hash(
        job_b, "google_careers"
    )


def test_title_change_produces_different_hash() -> None:
    base = {
        "id": "101",
        "organization": "Google",
        "location": "Mountain View, CA, USA",
        "raw_html": "<p>Build systems.</p>",
    }
    job_a = {**base, "title": "Software Engineer"}
    job_b = {**base, "title": "Senior Software Engineer"}
    assert compute_job_content_hash(job_a, "google_careers") != compute_job_content_hash(
        job_b, "google_careers"
    )


def test_location_suffix_stripped_for_hash() -> None:
    job_a = {
        "id": "101",
        "title": "Software Engineer",
        "organization": "Google",
        "location": "San Francisco, CA, USA",
        "raw_html": "<p>Build systems.</p>",
    }
    job_b = {
        **job_a,
        "location": "San Francisco, CA, USA; +24 more",
    }
    assert compute_job_content_hash(job_a, "google_careers") == compute_job_content_hash(
        job_b, "google_careers"
    )


def test_greenhouse_job_hash_ignores_volatile_dict_fields() -> None:
    job_a = {
        "id": 42,
        "title": "Backend Engineer",
        "location": {"name": "New York"},
        "departments": [{"name": "Engineering"}],
        "absolute_url": "https://boards.greenhouse.io/acme/jobs/42",
        "content": "<p>Build APIs.</p>",
        "updated_at": "2026-05-20T10:00:00Z",
    }
    job_b = {
        **job_a,
        "absolute_url": "https://boards.greenhouse.io/acme/jobs/42?utm=1",
        "updated_at": "2026-06-01T10:00:00Z",
    }
    assert compute_job_content_hash(job_a, "greenhouse") == compute_job_content_hash(
        job_b, "greenhouse"
    )


def test_google_fixture_list_fields_not_duplicated_when_detail_html_present() -> None:
    detail_html = (FIXTURES / "detail_page.html").read_text()
    job_with_detail = {
        "id": "143122286080074438",
        "title": "Forward Deployed Engineer IV, GenAI, Google Cloud",
        "organization": "Google",
        "location": "San Francisco, CA, USA",
        "raw_html": detail_html,
        "list_min_qualifications": "<li>different list-only content</li>",
    }
    job_without_list = {k: v for k, v in job_with_detail.items() if k != "list_min_qualifications"}
    assert compute_job_content_hash(job_with_detail, "google_careers") == compute_job_content_hash(
        job_without_list, "google_careers"
    )
