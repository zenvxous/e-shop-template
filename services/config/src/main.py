import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import get_settings
from src.routers import router

settings = get_settings()

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.service_name}...")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Config Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["System"])
@app.head("/health", tags=["System"])
async def health():
    return {"status": "healthy", "service": settings.service_name}