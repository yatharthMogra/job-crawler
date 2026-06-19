import json

from app.ingestion.fetch_schedule_config import parse_fetch_schedule_json


def test_parse_fetch_schedule_json_waas_and_throttles() -> None:
    raw = json.dumps(
        {
            "waas": {"dedicated_job": False, "interval_minutes": 45},
            "throttles": {"default_concurrency": 5, "platforms": {"ashby": {"concurrency": 1}}},
        }
    )
    schedule = parse_fetch_schedule_json(raw)
    assert schedule.waas.dedicated_job is False
    assert schedule.waas.interval_minutes == 45
    assert schedule.throttles.default_concurrency == 5
    assert schedule.throttles.for_platform("ashby").concurrency == 1
    assert schedule.throttles.for_platform("greenhouse").concurrency == 5
