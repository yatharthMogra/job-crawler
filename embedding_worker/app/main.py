from __future__ import annotations

import base64
import json
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.handlers.resume import ResumeEmbedOutcome, process_resume_embedding
from app.utils.logging import configure_logging

log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    yield


app = FastAPI(title="Embedding Worker", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


def _decode_pubsub_payload(envelope: dict) -> dict | None:
    message = envelope.get("message")
    if not isinstance(message, dict):
        return None
    raw_data = message.get("data")
    if not raw_data:
        return None
    decoded = base64.b64decode(raw_data).decode("utf-8")
    payload = json.loads(decoded)
    if not isinstance(payload, dict):
        return None
    return payload


@app.post("/")
async def handle_pubsub_push(request: Request) -> Response:
    try:
        envelope = await request.json()
    except Exception as exc:
        log.warning("pubsub_invalid_envelope", error=str(exc))
        return JSONResponse({"status": "invalid_envelope"}, status_code=400)

    payload = _decode_pubsub_payload(envelope)
    if payload is None:
        log.warning("pubsub_missing_payload")
        return JSONResponse({"status": "missing_payload"}, status_code=400)

    entity_type = payload.get("entity_type")
    entity_id_raw = payload.get("entity_id")
    if entity_type != "resume":
        log.info("pubsub_ignored_entity_type", entity_type=entity_type)
        return JSONResponse({"status": "ignored"}, status_code=200)

    try:
        resume_id = uuid.UUID(str(entity_id_raw))
    except (TypeError, ValueError):
        log.warning("pubsub_invalid_entity_id", entity_id=entity_id_raw)
        return JSONResponse({"status": "invalid_entity_id"}, status_code=200)

    try:
        outcome = await process_resume_embedding(resume_id)
    except Exception:
        log.exception("resume_embedding_handler_failed", resume_id=str(resume_id))
        return JSONResponse({"status": "error"}, status_code=500)

    if outcome == ResumeEmbedOutcome.TRANSIENT_ERROR:
        return JSONResponse({"status": "error"}, status_code=500)

    return JSONResponse({"status": "ok", "outcome": outcome.value}, status_code=200)
