from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionFactory
from src.repo.category import CategoryRepository
from src.repo.product import ProductRepository
from src.services.category import CategoryService
from src.services.product import ProductService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def get_category_service(
    session: AsyncSession = Depends(get_session),
) -> CategoryService:
    return CategoryService(CategoryRepository(session))


async def get_product_service(
    session: AsyncSession = Depends(get_session),
) -> ProductService:
    return ProductService(ProductRepository(session))
