from __future__ import annotations

import base64
import json
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.handlers.resume import ResumeEmbedOutcome
from app.main import _decode_pubsub_payload, app


def _pubsub_envelope(payload: dict) -> dict:
    encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    return {"message": {"data": encoded, "messageId": "1"}}


def test_decode_pubsub_payload() -> None:
    resume_id = str(uuid.uuid4())
    envelope = _pubsub_envelope({"entity_type": "resume", "entity_id": resume_id})
    decoded = _decode_pubsub_payload(envelope)
    assert decoded == {"entity_type": "resume", "entity_id": resume_id}


def test_decode_pubsub_payload_missing_data() -> None:
    assert _decode_pubsub_payload({"message": {}}) is None


def test_push_handler_ignores_non_resume_entity() -> None:
    client = TestClient(app)
    envelope = _pubsub_envelope({"entity_type": "job", "entity_id": str(uuid.uuid4())})
    response = client.post("/", json=envelope)
    assert response.status_code == 200
    assert response.json()["status"] == "ignored"


def test_push_handler_skips_already_embedded() -> None:
    client = TestClient(app)
    resume_id = uuid.uuid4()
    envelope = _pubsub_envelope({"entity_type": "resume", "entity_id": str(resume_id)})

    with patch("app.main.process_resume_embedding", new=AsyncMock(return_value=ResumeEmbedOutcome.SKIPPED)):
        response = client.post("/", json=envelope)

    assert response.status_code == 200
    assert response.json()["outcome"] == "skipped"


def test_push_handler_retries_on_transient_error() -> None:
    client = TestClient(app)
    resume_id = uuid.uuid4()
    envelope = _pubsub_envelope({"entity_type": "resume", "entity_id": str(resume_id)})

    with patch(
        "app.main.process_resume_embedding",
        new=AsyncMock(return_value=ResumeEmbedOutcome.TRANSIENT_ERROR),
    ):
        response = client.post("/", json=envelope)

    assert response.status_code == 500
