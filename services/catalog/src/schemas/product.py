import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductImageRead(BaseModel):
    id: uuid.UUID
    object_key: str
    is_main: bool

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(gt=0, decimal_places=2)
    stock: int = Field(ge=0)
    seller_id: uuid.UUID
    category_id: uuid.UUID | None = None


class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: uuid.UUID | None = None
    is_active: bool | None = None


class ProductRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    price: Decimal
    stock: int
    seller_id: uuid.UUID
    category_id: uuid.UUID | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    images: list[ProductImageRead] = []

    model_config = ConfigDict(from_attributes=True)


class ProductListItem(BaseModel):
    """Облегчённая схема для списка — без описания"""
    id: uuid.UUID
    title: str
    price: Decimal
    stock: int
    is_active: bool
    images: list[ProductImageRead] = []

    model_config = ConfigDict(from_attributes=True)


class PaginatedProducts(BaseModel):
    items: list[ProductListItem]
    total: int
    page: int
    limit: int
    pages: int
