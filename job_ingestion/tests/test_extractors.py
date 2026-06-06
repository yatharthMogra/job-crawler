from app.ingestion.extractor.deterministic import extract_deterministic_fields
from app.ingestion.extractor.text_cleaner import build_description_preview, clean_job_description


def test_clean_job_description_strips_html() -> None:
    html = "<p>Hello <strong>World</strong></p><div>Remote role</div>"
    assert clean_job_description(html) == "Hello World Remote role"


def test_clean_job_description_strips_escaped_html() -> None:
    escaped_html = "&lt;p&gt;Hello &lt;strong&gt;World&lt;/strong&gt;&lt;/p&gt;"
    assert clean_job_description(escaped_html) == "Hello World"


def test_clean_job_description_strips_double_escaped_html() -> None:
    double_escaped = "&amp;lt;p&amp;gt;Hello&amp;lt;/p&amp;gt;"
    assert clean_job_description(double_escaped) == "Hello"


def test_extract_deterministic_fields() -> None:
    raw_job = {
        "id": 42,
        "title": "Backend Engineer",
        "location": {"name": "New York"},
        "departments": [{"name": "Engineering"}],
        "absolute_url": "https://example.com/job/42",
        "updated_at": "2026-05-20T10:00:00Z",
        "metadata": [{"name": "Employment Type", "value": "Full-time"}],
    }

    fields = extract_deterministic_fields(raw_job)

    assert fields["external_job_id"] == "42"
    assert fields["title"] == "Backend Engineer"
    assert fields["location"] == "New York"
    assert fields["department"] == "Engineering"
    assert fields["employment_type"] == "Full-time"
    assert fields["posting_url"] == "https://example.com/job/42"
    assert fields["posted_at"] is not None


def test_build_description_preview_short_text() -> None:
    text = "Short job description."
    assert build_description_preview(text, max_chars=100) == text


def test_build_description_preview_truncates_word_boundary() -> None:
    text = "alpha beta gamma delta epsilon zeta eta theta iota kappa"
    preview = build_description_preview(text, max_chars=24)
    assert preview == "alpha beta gamma delta..."
