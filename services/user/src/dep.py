from typing import AsyncGenerator

from fastapi import Depends
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database import AsyncSessionFactory
from src.repo.address import AddressRepository
from src.repo.user import UserRepository
from src.services.address import AddressService
from src.services.user import UserService

settings = get_settings()


# ──────────── DB Session ────────────

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# ──────────── MinIO Client ────────────

def get_minio() -> Minio:
    return Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_use_ssl,
    )


# ──────────── Services ────────────

async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(UserRepository(session))


async def get_address_service(
    session: AsyncSession = Depends(get_session),
) -> AddressService:
    return AddressService(AddressRepository(session))
