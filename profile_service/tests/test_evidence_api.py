import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import get_settings
from app.main import app
from app.models.candidate import Candidate
from app.models.evidence import CandidateEvidence
from app.models.resume import CandidateResume


@pytest.fixture
def api_headers() -> dict[str, str]:
    return {"X-API-Key": get_settings().api_key}


def _sync_database_url() -> str:
    return get_settings().database_url.replace("+asyncpg", "+psycopg")


@pytest.mark.asyncio
async def test_list_evidence_approved_only(api_headers) -> None:
    candidate_id = uuid.uuid4()
    resume_id = uuid.uuid4()

    engine = create_engine(_sync_database_url())
    with Session(engine) as db:
        db.add(Candidate(id=candidate_id, email=f"ev-{uuid.uuid4()}@example.com", name="Evidence Test"))
        db.add(
            CandidateResume(
                id=resume_id,
                candidate_id=candidate_id,
                file_path="/tmp/test.pdf",
                original_filename="test.pdf",
                file_size_bytes=100,
                extraction_status="success",
            )
        )
        db.add(
            CandidateEvidence(
                candidate_id=candidate_id,
                source_resume_id=resume_id,
                evidence_type="experience",
                is_approved=True,
                is_active=True,
                normalized_data={"title": "Engineer", "company": "Acme"},
            )
        )
        db.add(
            CandidateEvidence(
                candidate_id=candidate_id,
                source_resume_id=resume_id,
                evidence_type="experience",
                is_approved=False,
                is_active=True,
                normalized_data={"title": "Intern", "company": "Beta"},
            )
        )
        db.commit()
    engine.dispose()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=api_headers) as client:
        response = await client.get(f"/candidates/{candidate_id}/evidence")

    assert response.status_code == 200
    body = response.json()
    assert len(body["evidence"]) == 1
    assert body["evidence"][0]["evidence_type"] == "experience"
