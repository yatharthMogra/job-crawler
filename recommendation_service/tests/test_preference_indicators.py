from __future__ import annotations

from types import SimpleNamespace

from app.scoring.preference_indicators import preference_indicators


def test_remote_and_salary_strengths() -> None:
    job = SimpleNamespace(
        location="Remote",
        job_country="US",
        remote_type="remote",
        salary_max=180_000,
    )
    profile = SimpleNamespace(
        preferences={"remote_preference": "remote"},
        constraints={"minimum_salary": 150_000},
    )

    indicators = preference_indicators(job, profile)

    assert [(item.label, item.kind) for item in indicators] == [
        ("Remote-friendly", "strength"),
        ("Meets salary expectations", "strength"),
    ]


def test_location_and_salary_gaps() -> None:
    job = SimpleNamespace(
        location="London, UK",
        job_country="GB",
        remote_type="onsite",
        salary_max=100_000,
    )
    profile = SimpleNamespace(
        preferences={"preferred_countries": ["US"]},
        constraints={"minimum_salary": 150_000},
    )

    indicators = preference_indicators(job, profile)

    assert [(item.label, item.kind) for item in indicators] == [
        ("Outside preferred location", "gap"),
        ("Below your salary minimum", "gap"),
    ]
