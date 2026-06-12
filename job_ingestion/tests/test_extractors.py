from datetime import timezone

from app.ingestion.extractor.deterministic import (
    _parse_workday_date,
    extract_deterministic_fields,
)
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


def test_parse_workday_date() -> None:
    parsed = _parse_workday_date("05/15/2026")
    assert parsed is not None
    assert parsed.year == 2026
    assert parsed.month == 5
    assert parsed.day == 15
    assert parsed.tzinfo == timezone.utc
    assert _parse_workday_date(None) is None
    assert _parse_workday_date("not-a-date") is None


def test_extract_workday_fields() -> None:
    raw_job = {
        "id": "JR-12345",
        "title": "Senior Software Engineer",
        "postedOn": "05/15/2026",
        "locationsText": "New York, NY, USA",
        "bulletFields": ["Full time"],
        "externalLink": "https://stripe.wd1.myworkdayjobs.com/job/New-York/SWE_JR-12345",
        "jobPostingInfo": {
            "title": "Senior Software Engineer",
            "jobReqId": "JR-12345",
            "jobDescription": "<p>Build APIs with Python.</p>",
            "location": "New York, NY, USA",
            "postedOn": "05/15/2026",
            "jobScheduleType": "Full_Time",
            "department": "Engineering",
        },
    }

    fields = extract_deterministic_fields(raw_job, platform="workday")

    assert fields["external_job_id"] == "JR-12345"
    assert fields["title"] == "Senior Software Engineer"
    assert fields["location"] == "New York, NY, USA"
    assert fields["department"] == "Engineering"
    assert fields["employment_type"] == "Full-time"
    assert fields["posting_url"] == raw_job["externalLink"]
    assert fields["posted_at"] is not None
    assert fields["raw_html"] == "<p>Build APIs with Python.</p>"


def test_workday_employment_type_mapping() -> None:
    for schedule, expected in [
        ("Full_Time", "Full-time"),
        ("Internship", "Internship"),
        ("Part_Time", "Part-time"),
    ]:
        fields = extract_deterministic_fields(
            {
                "id": "JR-1",
                "jobPostingInfo": {"jobScheduleType": schedule},
            },
            platform="workday",
        )
        assert fields["employment_type"] == expected

    fields = extract_deterministic_fields(
        {"id": "JR-2", "bulletFields": ["Contract role"], "jobPostingInfo": {}},
        platform="workday",
    )
    assert fields["employment_type"] == "Contract"

    fields = extract_deterministic_fields(
        {"id": "JR-3", "jobPostingInfo": {"jobScheduleType": "Unknown"}},
        platform="workday",
    )
    assert fields["employment_type"] is None


def test_parse_oracle_date() -> None:
    from app.ingestion.extractor.deterministic import _parse_oracle_date

    parsed = _parse_oracle_date("2026-05-20")
    assert parsed is not None
    assert parsed.year == 2026
    assert parsed.month == 5
    assert parsed.day == 20
    assert parsed.tzinfo == timezone.utc
    assert _parse_oracle_date(None) is None
    assert _parse_oracle_date("not-a-date") is None


def test_extract_oracle_hcm_fields() -> None:
    raw_job = {
        "id": "307750",
        "Title": "Software Engineer III",
        "PrimaryLocation": "New York, New York, United States",
        "otherWorkLocations": [{"Name": "Remote, United States"}],
        "PostedDate": "2026-05-20",
        "Category": "Information Technology",
        "ExternalDescriptionStr": "<p>Overview</p>",
        "ExternalQualificationsStr": "<ul><li>Python</li></ul>",
        "ExternalResponsibilitiesStr": "<ul><li>Build APIs</li></ul>",
        "requisitionFlexFields": [{"Prompt": "Employment Type", "Value": "Full Time"}],
        "externalLink": (
            "https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1"
            "/requisitions/307750/details"
        ),
    }

    fields = extract_deterministic_fields(raw_job, platform="oracle_hcm")

    assert fields["external_job_id"] == "307750"
    assert fields["title"] == "Software Engineer III"
    assert fields["location"] == "New York, New York, United States | Remote, United States"
    assert fields["department"] == "Information Technology"
    assert fields["employment_type"] == "Full Time"
    assert fields["posting_url"] == raw_job["externalLink"]
    assert fields["posted_at"] is not None
    assert fields["raw_html"] == (
        "<p>Overview</p>\n<ul><li>Python</li></ul>\n<ul><li>Build APIs</li></ul>"
    )


def test_oracle_description_concatenation_missing_fields() -> None:
    raw_job = {
        "id": "1",
        "Title": "Engineer",
        "ExternalDescriptionStr": "<p>Only overview</p>",
    }

    fields = extract_deterministic_fields(raw_job, platform="oracle_hcm")

    assert fields["raw_html"] == "<p>Only overview</p>"


def test_oracle_employment_type_workplace_fallback() -> None:
    fields = extract_deterministic_fields(
        {"id": "1", "Title": "Engineer", "WorkplaceType": "Remote"},
        platform="oracle_hcm",
    )
    assert fields["employment_type"] == "Remote"
