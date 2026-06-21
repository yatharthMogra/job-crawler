from __future__ import annotations

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

LOCAL_PORT = 8002

LOCAL_SERVICES = """
### Local API services

| Service | Base URL | Swagger |
|---------|----------|---------|
| Job Ingestion | http://localhost:8000 | http://localhost:8000/docs |
| Profile Service | http://localhost:8001 | http://localhost:8001/docs |
| **Recommendation Service** (this service) | http://localhost:8002 | [/docs](/docs) |

Dashboard routes require `candidate_id` query params. Notification worker also exposes `POST /notifications/run` when the scheduler is enabled.
"""

OPENAPI_TAGS = [
    {
        "name": "meta",
        "description": "Service health, discovery, and notification triggers.",
    },
    {
        "name": "dashboard",
        "description": "Personalized job feed, recommendations, applications, and job detail.",
    },
    {
        "name": "subscriptions",
        "description": "Retrieval pool subscriptions per candidate.",
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
                "Job recommendations, scoring, subscriptions, and notifications for Career Match AI.\n\n"
                + LOCAL_SERVICES
            ),
            routes=app.routes,
            servers=[{"url": f"http://localhost:{LOCAL_PORT}", "description": "Local dev"}],
            tags=OPENAPI_TAGS,
        )
        app.openapi_schema = schema
        return schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
