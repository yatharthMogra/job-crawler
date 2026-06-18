from datetime import timezone

from app.ingestion.extractor.deterministic import (
    _parse_icims_date,
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


def test_parse_icims_date() -> None:
    parsed_date = _parse_icims_date("2026-06-05")
    assert parsed_date is not None
    assert parsed_date.year == 2026
    assert parsed_date.month == 6
    assert parsed_date.day == 5
    assert parsed_date.tzinfo == timezone.utc

    parsed_iso = _parse_icims_date("2026-06-05T14:23:00+00:00")
    assert parsed_iso is not None
    assert parsed_iso.hour == 14
    assert parsed_iso.minute == 23

    assert _parse_icims_date(None) is None
    assert _parse_icims_date("not-a-date") is None


def test_extract_icims_fields() -> None:
    raw_job = {
        "id": "6414",
        "title": "Finance Project Analyst",
        "location": "US-CA-Menlo Park",
        "department": "Accounting/Finance",
        "employment_type_raw": "Full-Time",
        "raw_html": "<p>Overview content.</p>",
        "sitemap_url": "https://careers-sri.icims.com/jobs/6414/finance-project-analyst/job",
        "detail_url": (
            "https://careers-sri.icims.com/jobs/6414/finance-project-analyst/job?in_iframe=1"
        ),
        "lastmod": "2026-06-05T16:53:18-04:00",
    }

    fields = extract_deterministic_fields(raw_job, platform="icims")

    assert fields["external_job_id"] == "6414"
    assert fields["title"] == "Finance Project Analyst"
    assert fields["location"] == "US-CA-Menlo Park"
    assert fields["department"] == "Accounting/Finance"
    assert fields["employment_type"] == "Full-time"
    assert fields["posting_url"] == raw_job["sitemap_url"]
    assert "?in_iframe=1" not in fields["posting_url"]
    assert fields["posted_at"] is not None
    assert fields["raw_html"] == "<p>Overview content.</p>"


def test_icims_employment_type_mapping() -> None:
    assert (
        extract_deterministic_fields(
            {"id": "1", "employment_type_raw": "Intern"},
            platform="icims",
        )["employment_type"]
        == "Internship"
    )
    assert (
        extract_deterministic_fields(
            {"id": "1", "employment_type_raw": "Temporary Part-Time"},
            platform="icims",
        )["employment_type"]
        == "Part-time"
    )


def test_extract_workable_fields() -> None:
    raw_job = {
        "id": "48DBFB8E87",
        "title": "AI Applications Engineer",
        "employment_type": "Full-time",
        "department": "Software Engineering",
        "url": "https://apply.workable.com/j/48DBFB8E87",
        "published_on": "2025-08-25",
        "telecommuting": False,
        "locations": [
            {
                "country": "United States",
                "city": "Burlingame",
                "region": "California",
            }
        ],
        "description": "Build AI applications on Quadric hardware.",
    }

    fields = extract_deterministic_fields(raw_job, platform="workable")

    assert fields["external_job_id"] == "48DBFB8E87"
    assert fields["title"] == "AI Applications Engineer"
    assert fields["location"] == "Burlingame, California, United States"
    assert fields["department"] == "Software Engineering"
    assert fields["employment_type"] == "Full-time"
    assert fields["posting_url"] == "https://apply.workable.com/j/48DBFB8E87"
    assert fields["posted_at"] is not None
    assert fields["raw_html"] == "Build AI applications on Quadric hardware."


def test_extract_workable_remote_location() -> None:
    fields = extract_deterministic_fields(
        {
            "id": "36FEA4E309",
            "title": "Field Application Engineer",
            "telecommuting": True,
            "locations": [{"country": "Israel", "countryCode": "IL"}],
        },
        platform="workable",
    )
    assert fields["location"] == "Remote | Israel"


def test_extract_workable_multi_location() -> None:
    fields = extract_deterministic_fields(
        {
            "id": "B463DB2082",
            "title": "Field Application Engineer",
            "telecommuting": True,
            "locations": [
                {"country": "China", "countryCode": "CN"},
                {"country": "Taiwan", "countryCode": "TW"},
            ],
        },
        platform="workable",
    )
    assert fields["location"] == "Remote | China | Taiwan"


def test_extract_job_country() -> None:
    from app.ingestion.extractor.deterministic import extract_job_country

    assert extract_job_country("New York, NY, USA") == "US"
    assert extract_job_country("Gurugram, HR, India") == "IN"
    assert extract_job_country("Pune City, Maharashtra, India") == "IN"
    assert extract_job_country("Toronto, ON, Canada") == "CA"
    assert extract_job_country("Remote - US") is None
    assert extract_job_country("Berlin, Germany") == "DE"
    assert extract_job_country("US-CA-Menlo Park") == "US"
    assert extract_job_country(None) is None
    assert extract_job_country("Unknown City") is None
    assert extract_job_country("AUSTIN, TX") == "US"
    assert extract_job_country("Manulife Tower, Manulife (Singapore) Pte Ltd") == "SG"
    assert extract_job_country("Fab 10A, Singapore") == "SG"
    assert extract_job_country("Hong Kong") == "HK"


def test_icims_posting_url_no_iframe_param() -> None:
    fields = extract_deterministic_fields(
        {
            "id": "1",
            "detail_url": "https://careers-sri.icims.com/jobs/1/example/job?in_iframe=1",
        },
        platform="icims",
    )
    assert fields["posting_url"] == "https://careers-sri.icims.com/jobs/1/example/job"


def test_extract_workatastartup_fields() -> None:
    raw_job = {
        "id": "yc_123",
        "title": "Senior Backend Engineer",
        "location": "San Francisco, CA",
        "remote": False,
        "description": "<p>Build systems</p>",
        "apply_url": "https://www.workatastartup.com/jobs/123",
        "created_at": "2026-06-10T18:00:00Z",
        "job_type": "fulltime",
        "company": {"name": "Acme AI", "slug": "acme-ai", "batch": "S24"},
    }
    fields = extract_deterministic_fields(raw_job, platform="workatastartup")
    assert fields["external_job_id"] == "yc_123"
    assert fields["title"] == "Senior Backend Engineer"
    assert fields["location"] == "San Francisco, CA"
    assert fields["company_name"] == "Acme AI"
    assert fields["employment_type"] == "Full-time"
    assert fields["job_country"] == "US"
    assert fields["posting_url"] == "https://www.workatastartup.com/jobs/123"
