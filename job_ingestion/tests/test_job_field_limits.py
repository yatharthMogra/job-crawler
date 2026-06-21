from app.ingestion.job_field_limits import clamp_deterministic_fields, clamp_str


def test_clamp_str_truncates_long_values() -> None:
    assert clamp_str("a" * 300, 255) == "a" * 255
    assert clamp_str("short", 255) == "short"
    assert clamp_str(None, 255) is None


def test_clamp_deterministic_fields_applies_column_limits() -> None:
    fields = clamp_deterministic_fields(
        {
            "external_job_id": "x" * 300,
            "title": "t" * 600,
            "company_name": "Amazon",
            "location": "l" * 400,
            "department": "d" * 300,
            "employment_type": "e" * 300,
            "dedup_fingerprint": "f" * 250,
            "posting_url": "https://example.com",
        }
    )
    assert len(fields["external_job_id"]) == 255
    assert len(fields["title"]) == 512
    assert len(fields["location"]) == 255
    assert len(fields["department"]) == 255
    assert len(fields["employment_type"]) == 255
    assert len(fields["dedup_fingerprint"]) == 200
    assert fields["posting_url"] == "https://example.com"
