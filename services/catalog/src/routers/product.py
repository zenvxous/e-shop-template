import uuid
from fastapi import APIRouter, Depends, Query, status

from src.dep import get_product_service
from src.schemas.product import (
    ProductCreate, ProductRead, ProductUpdate, PaginatedProducts,
)
from src.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=PaginatedProducts)
async def list_products(
    category_id: uuid.UUID | None = Query(default=None),
    seller_id: uuid.UUID | None = Query(default=None),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
):
    return await service.list_products(
        category_id=category_id,
        seller_id=seller_id,
        min_price=min_price,
        max_price=max_price,
        page=page,
        limit=limit,
    )


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    return await service.get(product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return await service.create(data)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return await service.update(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    await service.delete(product_id)


@router.post("/{product_id}/images", response_model=ProductRead)
async def add_image(
    product_id: uuid.UUID,
    object_key: str,
    is_main: bool = False,
    service: ProductService = Depends(get_product_service),
):
    return await service.add_image(product_id, object_key, is_main)


@router.delete(
    "/{product_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_image(
    product_id: uuid.UUID,
    image_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    await service.delete_image(product_id, image_id)
