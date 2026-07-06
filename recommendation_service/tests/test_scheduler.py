from app.config import Settings
from app.scheduler import create_scheduler


def test_scheduler_registers_digest_and_company_watch_jobs() -> None:
    settings = Settings(
        digest_scheduler_poll_minutes=15,
        company_watch_poll_minutes=3,
    )
    scheduler = create_scheduler(settings)
    job_ids = {job.id for job in scheduler.get_jobs()}
    assert job_ids == {"digest_scheduler", "company_watch_processor", "company_watch_batch_processor"}
