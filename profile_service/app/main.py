from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.candidates import router as candidates_router
from app.api.profiles import router as profiles_router
from app.auth import require_api_key
from app.config import get_settings
from app.utils.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    yield


settings = get_settings()
app = FastAPI(title="Profile Service", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates_router)
app.include_router(profiles_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/protected-health", dependencies=[Depends(require_api_key)])
async def protected_health() -> dict[str, str]:
    return {"status": "authenticated"}
