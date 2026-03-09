from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from src.config import get_settings
from src.database import engine, Base
from src.routers import category, product

settings = get_settings()

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.service_name}...")

    # Создаём таблицы (в prod используй Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables ready")
    yield

    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title="Catalog Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(category.router)
app.include_router(product.router)


@app.get("/health", tags=["System"])
async def health():
    return {"status": "healthy", "service": settings.service_name}
