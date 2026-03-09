import uuid
import math
from fastapi import HTTPException

from src.repo.product import ProductRepository
from src.schemas.product import (
    ProductCreate, ProductRead, ProductUpdate,
    PaginatedProducts, ProductListItem,
)


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def create(self, data: ProductCreate) -> ProductRead:
        product = await self.repo.create(data)
        return ProductRead.model_validate(product)

    async def get(self, product_id: uuid.UUID) -> ProductRead:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductRead.model_validate(product)

    async def list_products(
        self,
        category_id: uuid.UUID | None,
        seller_id: uuid.UUID | None,
        min_price: float | None,
        max_price: float | None,
        page: int,
        limit: int,
    ) -> PaginatedProducts:
        products, total = await self.repo.get_list(
            category_id=category_id,
            seller_id=seller_id,
            min_price=min_price,
            max_price=max_price,
            page=page,
            limit=limit,
        )
        return PaginatedProducts(
            items=[ProductListItem.model_validate(p) for p in products],
            total=total,
            page=page,
            limit=limit,
            pages=math.ceil(total / limit) if total else 0,
        )

    async def update(self, product_id: uuid.UUID, data: ProductUpdate) -> ProductRead:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product = await self.repo.update(product, data)
        return ProductRead.model_validate(product)

    async def delete(self, product_id: uuid.UUID) -> None:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await self.repo.delete(product)

    async def add_image(
        self,
        product_id: uuid.UUID,
        object_key: str,
        is_main: bool = False,
    ) -> ProductRead:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await self.repo.add_image(product, object_key, is_main)
        # Refresh product
        product = await self.repo.get_by_id(product_id)
        return ProductRead.model_validate(product)

    async def delete_image(
        self, product_id: uuid.UUID, image_id: uuid.UUID
    ) -> None:
        image = await self.repo.get_image(image_id)
        if not image or image.product_id != product_id:
            raise HTTPException(status_code=404, detail="Image not found")
        await self.repo.delete_image(image)
