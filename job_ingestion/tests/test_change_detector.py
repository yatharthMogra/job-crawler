from app.ingestion.change_detector import classify_jobs
from app.utils.hashing import compute_content_hash


def test_classify_jobs_new_updated_unchanged_and_removed() -> None:
    unchanged_job = {"id": 1, "title": "Software Engineer"}
    updated_job_old = {"id": 2, "title": "Data Engineer"}
    updated_job_new = {"id": 2, "title": "Senior Data Engineer"}
    new_job = {"id": 3, "title": "ML Engineer"}

    previous_hashes = {
        "1": compute_content_hash(unchanged_job),
        "2": compute_content_hash(updated_job_old),
        "4": "old_hash",
    }
    previously_active_ids = {"1", "2", "4"}

    result = classify_jobs(
        fetched_jobs=[unchanged_job, updated_job_new, new_job],
        previous_hashes=previous_hashes,
        previously_active_job_ids=previously_active_ids,
    )

    assert len(result.new) == 1
    assert len(result.updated) == 1
    assert len(result.unchanged) == 1
    assert result.removed_ids == ["4"]
