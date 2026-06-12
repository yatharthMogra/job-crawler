import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.companies import router as companies_router
from app.api.enrichment import compat_router as enrichments_router
from app.api.enrichment import router as enrichment_router
from app.api.events import router as events_router
from app.api.jobs import router as jobs_router
from app.api.maintenance import router as maintenance_router
from app.api.pipeline import router as pipeline_router
from app.api.reprocessing import router as reprocessing_router
from app.config import get_settings
from app.utils.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    from app.ingestion.constants import EventType
    from app.ingestion.enrichment_worker import get_enrichment_worker
    from app.scheduler import build_scheduler, emit_scheduler_event

    settings = get_settings()
    configure_logging(settings.log_level)
    scheduler = build_scheduler(settings)
    enrichment_worker = get_enrichment_worker(settings=settings)
    scheduler.start()
    worker_task = asyncio.create_task(enrichment_worker.run_forever())
    await emit_scheduler_event(EventType.SCHEDULER_STARTED)
    try:
        yield
    finally:
        enrichment_worker.stop()
        if worker_task is not None:
            await worker_task
        scheduler.shutdown(wait=False)
        await emit_scheduler_event(EventType.SCHEDULER_STOPPED)


app = FastAPI(title="Job Ingestion", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)
app.include_router(companies_router)
app.include_router(pipeline_router)
app.include_router(reprocessing_router)
app.include_router(events_router)
app.include_router(jobs_router)
app.include_router(enrichment_router)
app.include_router(enrichments_router)
app.include_router(maintenance_router)
