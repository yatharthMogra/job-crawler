from app.ingestion.change_detector import classify_jobs
from app.ingestion.job_content_hash import compute_job_content_hash


def test_classify_jobs_new_updated_unchanged_and_removed() -> None:
    unchanged_job = {"id": 1, "title": "Software Engineer", "content": "<p>Build APIs</p>"}
    updated_job_old = {"id": 2, "title": "Data Engineer", "content": "<p>ETL pipelines</p>"}
    updated_job_new = {"id": 2, "title": "Senior Data Engineer", "content": "<p>ETL pipelines</p>"}
    new_job = {"id": 3, "title": "ML Engineer", "content": "<p>Models</p>"}
    platform = "greenhouse"

    previous_hashes = {
        "1": compute_job_content_hash(unchanged_job, platform),
        "2": compute_job_content_hash(updated_job_old, platform),
        "4": "old_hash",
    }
    previously_active_ids = {"1", "2", "4"}

    result = classify_jobs(
        fetched_jobs=[unchanged_job, updated_job_new, new_job],
        previous_hashes=previous_hashes,
        previously_active_job_ids=previously_active_ids,
        platform=platform,
    )

    assert len(result.new) == 1
    assert len(result.updated) == 1
    assert len(result.unchanged) == 1
    assert result.removed_ids == ["4"]
