import asyncio
import logging
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
from app.api.stats import router as stats_router
from app.config import get_settings
from app.utils.logging import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    from app.ingestion.constants import EventType
    from app.ingestion.enrichment_worker import get_enrichment_worker_pool
    from app.ingestion.stats_publisher import publish_ops_stats_standalone
    from app.scheduler import build_scheduler, emit_scheduler_event

    settings = get_settings()
    configure_logging(settings.log_level)
    keys = settings.gemini_api_keys_list()
    if not keys:
        raise RuntimeError(
            "No Gemini API keys configured. Set GEMINI_API_KEYS or GEMINI_API_KEY in .env."
        )
    worker_count = settings.resolved_enrichment_worker_count()
    pool = get_enrichment_worker_pool(settings=settings)
    logger.info(
        "Starting enrichment pool: workers=%s keys=%s model=%s",
        worker_count,
        len(keys),
        settings.gemini_model,
    )
    scheduler = build_scheduler(settings)
    scheduler.start()
    worker_tasks = [asyncio.create_task(worker.run_forever()) for worker in pool.workers]
    await emit_scheduler_event(EventType.SCHEDULER_STARTED)
    try:
        await publish_ops_stats_standalone(settings=settings, trigger="startup")
        yield
    finally:
        pool.stop()
        if worker_tasks:
            await asyncio.gather(*worker_tasks, return_exceptions=True)
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
app.include_router(stats_router)
