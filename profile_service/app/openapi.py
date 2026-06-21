from __future__ import annotations

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

LOCAL_PORT = 8001

LOCAL_SERVICES = """
### Local API services

| Service | Base URL | Swagger |
|---------|----------|---------|
| Job Ingestion | http://localhost:8000 | http://localhost:8000/docs |
| **Profile Service** (this service) | http://localhost:8001 | [/docs](/docs) |
| Recommendation Service | http://localhost:8002 | http://localhost:8002/docs |

Most routes require the `X-API-Key` header (see **Authorize** in Swagger). Default dev key is in `.env.example`.
"""

OPENAPI_TAGS = [
    {
        "name": "meta",
        "description": "Service health and discovery.",
    },
    {
        "name": "candidates",
        "description": "Candidate accounts, OAuth upsert, email lookup, and resume upload.",
    },
    {
        "name": "profiles",
        "description": "Profile versions, patches, evidence, capabilities, and preference edits.",
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
                "Candidate profiles, resume parsing, and patch workflow for Career Match AI.\n\n"
                + LOCAL_SERVICES
            ),
            routes=app.routes,
            servers=[{"url": f"http://localhost:{LOCAL_PORT}", "description": "Local dev"}],
            tags=OPENAPI_TAGS,
        )
        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
