from dataclasses import dataclass, field
from typing import Any

from app.utils.hashing import compute_content_hash


@dataclass
class ClassifiedJobs:
    new: list[dict[str, Any]] = field(default_factory=list)
    updated: list[dict[str, Any]] = field(default_factory=list)
    unchanged: list[dict[str, Any]] = field(default_factory=list)
    removed_ids: list[str] = field(default_factory=list)
    hashes: dict[str, str] = field(default_factory=dict)


def classify_jobs(
    fetched_jobs: list[dict[str, Any]],
    previous_hashes: dict[str, str],
    previously_active_job_ids: set[str],
) -> ClassifiedJobs:
    result = ClassifiedJobs()
    seen_ids: set[str] = set()

    for job in fetched_jobs:
        external_job_id = str(job.get("id"))
        if not external_job_id or external_job_id == "None":
            continue

        seen_ids.add(external_job_id)
        content_hash = compute_content_hash(job)
        result.hashes[external_job_id] = content_hash
        old_hash = previous_hashes.get(external_job_id)

        if old_hash is None:
            result.new.append(job)
        elif old_hash != content_hash:
            result.updated.append(job)
        else:
            result.unchanged.append(job)

    result.removed_ids = sorted(previously_active_job_ids - seen_ids)
    return result
