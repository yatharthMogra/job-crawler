from __future__ import annotations

import json
import uuid
from functools import lru_cache

import structlog
from google.cloud import pubsub_v1

from app.config import get_settings

log = structlog.get_logger(__name__)


@lru_cache(maxsize=1)
def _publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def publish_resume_embedding_request(resume_id: uuid.UUID) -> None:
    settings = get_settings()
    if not settings.should_publish_embedding_requests:
        return

    topic_path = _publisher().topic_path(
        settings.gcp_project.strip(),
        settings.embedding_requests_topic,
    )
    payload = json.dumps({"entity_type": "resume", "entity_id": str(resume_id)}).encode("utf-8")
    future = _publisher().publish(topic_path, payload)
    message_id = future.result(timeout=10)
    log.info("embedding_request_published", resume_id=str(resume_id), message_id=message_id)
