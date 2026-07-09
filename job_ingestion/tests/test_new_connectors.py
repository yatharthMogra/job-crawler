from __future__ import annotations

import pytest

from app.ingestion.connectors.talentbrew import (
    parse_talentbrew_detail_html,
    parse_talentbrew_list_page,
)
from app.ingestion.connectors.apple_careers import (
    SITE_ROOT,
    parse_apple_careers_detail_html,
    parse_apple_careers_list_page,
)
from app.ingestion.extractor.deterministic import extract_deterministic_fields


def test_parse_talentbrew_list_page() -> None:
    html = """
    <html><body>
      <a href="/job/mumbai/lead-data-engineer/45831/967847">Lead Data Engineer</a>
      <a href="/job/paris/senior-engineer/45831/916294">Senior Engineer</a>
      <span>page 1 / 6</span>
    </body></html>
    """
    summaries, total_pages = parse_talentbrew_list_page(
        html,
        base_url="https://careers.blackrock.com",
        company_id="45831",
    )
    assert total_pages == 6
    assert len(summaries) == 2
    assert summaries[0]["id"] == "967847"
    assert summaries[0]["externalLink"].endswith("/job/mumbai/lead-data-engineer/45831/967847")


def test_parse_talentbrew_detail_html() -> None:
    html = """
    <html><body>
      <div class="section2__main-container-description">
        <p>Build data pipelines.</p>
      </div>
    </body></html>
    """
    parsed = parse_talentbrew_detail_html(html)
    assert "Build data pipelines." in parsed["raw_html"]


def test_parse_apple_careers_list_page() -> None:
    html = """
    <html><body>
      <li class="job-list-item">
        <a href="/en-us/details/200668721-3337/distributed-systems-engineer?team=SFTWR"
           aria-label="Distributed Systems Engineer 200668721">
        </a>
        <span>May 07, 2026</span>
      </li>
    </body></html>
    """
    summaries = parse_apple_careers_list_page(
        html,
        base_url=SITE_ROOT,
    )
    assert len(summaries) == 1
    assert summaries[0]["id"] == "200668721-3337"
    assert summaries[0]["title"] == "Distributed Systems Engineer"
    assert summaries[0]["externalLink"].startswith("https://jobs.apple.com/en-us/details/")
    assert summaries[0]["posted_at"].year == 2026
    assert summaries[0]["posted_at"].month == 5


def test_parse_apple_posted_date() -> None:
    from app.ingestion.connectors.apple_careers import parse_apple_posted_date

    parsed = parse_apple_posted_date("May 07, 2026")
    assert parsed is not None
    assert parsed.year == 2026
    assert parse_apple_posted_date("") is None


def test_parse_apple_careers_detail_html() -> None:
    html = """
    <html><body>
      <h3>Summary</h3><p>Join our team.</p>
      <h3>Minimum Qualifications</h3><ul><li>BS in CS</li></ul>
    </body></html>
    """
    parsed = parse_apple_careers_detail_html(html)
    assert "Join our team." in parsed["raw_html"]
    assert "Minimum Qualifications" in parsed["raw_html"]


def test_extract_apple_careers_fields() -> None:
    from datetime import datetime, timezone

    posted_at = datetime(2026, 5, 7, tzinfo=timezone.utc)
    fields = extract_deterministic_fields(
        {
            "id": "200668721-3337",
            "title": "Distributed Systems Engineer",
            "location": "Cupertino",
            "externalLink": "https://jobs.apple.com/en-us/details/200668721-3337/engineer",
            "posted_at": posted_at,
            "raw_html": "<p>Description</p>",
        },
        platform="apple_careers",
    )
    assert fields["external_job_id"] == "200668721-3337"
    assert fields["posted_at"] == posted_at


def test_extract_talentbrew_fields() -> None:
    fields = extract_deterministic_fields(
        {
            "id": "967847",
            "title": "Lead Data Engineer",
            "location": "Mumbai, India",
            "externalLink": "https://careers.blackrock.com/job/mumbai/lead-data-engineer/45831/967847",
            "raw_html": "<p>Description</p>",
        },
        platform="talentbrew",
    )
    assert fields["external_job_id"] == "967847"
    assert fields["title"] == "Lead Data Engineer"
    assert fields["posting_url"].endswith("967847")


def test_extract_eightfold_fields() -> None:
    fields = extract_deterministic_fields(
        {
            "id": 755956726965,
            "name": "Data Scientist",
            "location": "New York, NY",
            "department": "Information Technology",
            "externalLink": "https://career.mlp.com/careers/job/755956726965?domain=mlp.com",
            "job_description": "<p>Build models.</p>",
            "t_create": 1781654400,
        },
        platform="eightfold",
    )
    assert fields["external_job_id"] == "755956726965"
    assert fields["title"] == "Data Scientist"
    assert fields["raw_html"] == "<p>Build models.</p>"
    assert fields["posted_at"] is not None
