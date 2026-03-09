import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import get_settings
from src.database import Base, engine
from src.routers import address, user

settings = get_settings()

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.service_name}...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables ready")
    yield

    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title="User Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(user.router)
app.include_router(address.router)


@app.get("/health", tags=["System"])
async def health():
    return {"status": "healthy", "service": settings.service_name}
