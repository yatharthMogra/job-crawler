from app.config import Settings, pipeline_interval_kwargs


def test_pipeline_interval_kwargs_uses_minutes_when_set() -> None:
    settings = Settings(fetch_cadence_minutes=30, fetch_cadence_hours=6)
    assert pipeline_interval_kwargs(settings) == {"minutes": 30}


def test_pipeline_interval_kwargs_falls_back_to_hours() -> None:
    settings = Settings(fetch_cadence_minutes=None, fetch_cadence_hours=6)
    assert pipeline_interval_kwargs(settings) == {"hours": 6}
