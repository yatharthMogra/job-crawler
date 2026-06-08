from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.subscriptions import router as subscriptions_router
from app.config import get_settings
from app.notification.pipeline import run_notification_pipeline
from app.scheduler import create_scheduler

_scheduler: AsyncIOScheduler | None = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    global _scheduler
    settings = get_settings()
    _scheduler = create_scheduler(settings)
    _scheduler.start()
    yield
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None


settings = get_settings()
app = FastAPI(title="Recommendation Service", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(subscriptions_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/notifications/run")
async def trigger_notification_pipeline() -> dict[str, str]:
    asyncio.create_task(run_notification_pipeline())
    return {"status": "started"}
