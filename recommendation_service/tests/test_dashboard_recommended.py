"""Lightweight tests for recommended jobs response helpers / legacy path wiring."""

from __future__ import annotations

from app.schemas.dashboard import DashboardRecommendedJobsResponse


def test_recommended_response_schema_has_reference_token() -> None:
    resp = DashboardRecommendedJobsResponse(
        jobs=[],
        total=0,
        reference_token="abc",
        offset=0,
        has_more=False,
        returned=0,
        total_ranked=10,
    )
    assert resp.reference_token == "abc"
    assert resp.total_ranked == 10
    assert resp.has_more is False


def test_recommended_response_defaults() -> None:
    resp = DashboardRecommendedJobsResponse(jobs=[])
    assert resp.reference_token is None
    assert resp.offset == 0
    assert resp.next_cursor is None
