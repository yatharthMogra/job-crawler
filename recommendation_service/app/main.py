from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.subscriptions import router as subscriptions_router
from app.config import get_settings
from app.notification.pipeline import run_notification_pipeline
from app.openapi import configure_openapi
from app.scheduler import create_scheduler

_scheduler: AsyncIOScheduler | None = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    global _scheduler
    settings = get_settings()
    if settings.enable_notification_scheduler:
        _scheduler = create_scheduler(settings)
        _scheduler.start()
    yield
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None


settings = get_settings()
app = FastAPI(title="Recommendation Service", lifespan=lifespan)
configure_openapi(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(subscriptions_router)


@app.get("/", tags=["meta"])
async def root() -> dict[str, str]:
    return {
        "service": "recommendation-service",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/health",
    }


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/notifications/run", tags=["meta"])
async def trigger_notification_pipeline() -> dict[str, str]:
    if not get_settings().enable_notification_scheduler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification pipeline is disabled on this deployment",
        )
    asyncio.create_task(run_notification_pipeline())
    return {"status": "started"}
