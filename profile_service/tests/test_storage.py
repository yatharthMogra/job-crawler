import uuid

import pytest

from app.config import Settings
from app.storage.base import resume_storage_key
from app.storage.local import LocalResumeStorage


def test_resume_storage_key_format() -> None:
    candidate_id = uuid.UUID("00000000-0000-4000-8000-000000000001")
    resume_id = uuid.UUID("00000000-0000-4000-8000-000000000002")
    assert resume_storage_key(candidate_id, resume_id) == (
        "00000000-0000-4000-8000-000000000001/00000000-0000-4000-8000-000000000002.pdf"
    )


def test_local_resume_storage_round_trip(tmp_path) -> None:
    settings = Settings(resume_storage_path=str(tmp_path))
    storage = LocalResumeStorage(settings)
    candidate_id = uuid.uuid4()
    resume_id = uuid.uuid4()
    content = b"%PDF-1.4 test content"

    key = storage.save(candidate_id, resume_id, content)
    assert key == resume_storage_key(candidate_id, resume_id)
    assert storage.read_bytes(key) == content
