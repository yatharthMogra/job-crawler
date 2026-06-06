from app.ingestion.pipeline import _resolve_terminal_status


def test_resolve_terminal_status_completed() -> None:
    assert _resolve_terminal_status(successful_companies=2, failed_companies=0) == "completed"


def test_resolve_terminal_status_partial_success() -> None:
    assert _resolve_terminal_status(successful_companies=1, failed_companies=1) == "partial_success"


def test_resolve_terminal_status_failed() -> None:
    assert _resolve_terminal_status(successful_companies=0, failed_companies=2) == "failed"
