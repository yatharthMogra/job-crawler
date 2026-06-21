from __future__ import annotations

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

LOCAL_PORT = 8000

LOCAL_SERVICES = """
### Local API services

| Service | Base URL | Swagger |
|---------|----------|---------|
| **Job Ingestion** (this service) | http://localhost:8000 | [/docs](/docs) |
| Profile Service | http://localhost:8001 | http://localhost:8001/docs |
| Recommendation Service | http://localhost:8002 | http://localhost:8002/docs |

Start locally with `./scripts/dev-job-ingestion.sh`, `./scripts/dev-profile-service.sh`, and `./scripts/dev-recommendation-service.sh`.
"""

OPENAPI_TAGS = [
    {
        "name": "meta",
        "description": "Service health and discovery.",
    },
    {
        "name": "stats",
        "description": "Aggregate ops snapshot: jobs, fetch, enrichment queue, backpressure.",
    },
    {
        "name": "pipeline",
        "description": "Trigger fetches and inspect pipeline run history.",
    },
    {
        "name": "companies",
        "description": "Company catalog, seed sync from companies.json, fetch tier and review flags.",
    },
    {
        "name": "jobs",
        "description": "Normalized jobs: list, detail, raw payload, reviewer edits, enrich-now.",
    },
    {
        "name": "enrichment",
        "description": "Enrichment queue, batches, per-job history, and LLM usage/cost (`/enrichment/*` and `/enrichments/*`).",
    },
    {
        "name": "events",
        "description": "Ingestion event stream and summaries.",
    },
    {
        "name": "reprocessing",
        "description": "Bulk re-enrichment by filters and reprocessing run history.",
    },
    {
        "name": "maintenance",
        "description": "Archival cleanup and enrichment queue maintenance.",
    },
    {
        "name": "admin",
        "description": "Taxonomy health, H-1B admin, and internal ops endpoints.",
    },
]


def configure_openapi(app: FastAPI) -> None:
    app.openapi_tags = OPENAPI_TAGS

    def custom_openapi() -> dict:
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title=app.title,
            version="1.0.0",
            description=(
                "Job board ingestion, enrichment, and ops APIs for Career Match AI.\n\n"
                + LOCAL_SERVICES
            ),
            routes=app.routes,
            servers=[{"url": f"http://localhost:{LOCAL_PORT}", "description": "Local dev"}],
            tags=OPENAPI_TAGS,
        )
        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
