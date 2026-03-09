import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product import Product, ProductImage
from src.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        *,
        category_id: uuid.UUID | None = None,
        seller_id: uuid.UUID | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        only_active: bool = True,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Product], int]:
        # Базовый запрос
        query = select(Product)

        # Фильтры
        if only_active:
            query = query.where(Product.is_active.is_(True))
        if category_id:
            query = query.where(Product.category_id == category_id)
        if seller_id:
            query = query.where(Product.seller_id == seller_id)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)

        # Считаем общее количество
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query) or 0

        # Пагинация
        query = query.order_by(Product.created_at.desc())
        query = query.offset((page - 1) * limit).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all()), total

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        product.is_active = False  # soft delete
        await self.session.commit()

    async def add_image(
        self,
        product: Product,
        object_key: str,
        is_main: bool = False,
    ) -> ProductImage:
        # Если новая картинка главная — снимаем флаг с остальных
        if is_main:
            for img in product.images:
                img.is_main = False

        image = ProductImage(
            product_id=product.id,
            object_key=object_key,
            is_main=is_main,
        )
        self.session.add(image)
        await self.session.commit()
        await self.session.refresh(image)
        return image

    async def delete_image(self, image: ProductImage) -> None:
        await self.session.delete(image)
        await self.session.commit()

    async def get_image(self, image_id: uuid.UUID) -> ProductImage | None:
        result = await self.session.execute(
            select(ProductImage).where(ProductImage.id == image_id)
        )
        return result.scalar_one_or_none()
