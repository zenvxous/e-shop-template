import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ──────────── Seller Profile ────────────

class SellerProfileRead(BaseModel):
    id: uuid.UUID
    shop_name: str
    description: str | None
    logo_key: str | None
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class BecomeSellerRequest(BaseModel):
    shop_name: str
    description: str | None = None


class SellerProfileUpdate(BaseModel):
    shop_name: str | None = None
    description: str | None = None


# ──────────── User ────────────

class UserCreate(BaseModel):
    """Вызывается при синхронизации с Keycloak"""
    keycloak_id: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class UserRead(BaseModel):
    id: uuid.UUID
    keycloak_id: str
    email: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    avatar_key: str | None
    is_seller: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    seller_profile: SellerProfileRead | None = None

    model_config = ConfigDict(from_attributes=True)


class UserPublicRead(BaseModel):
    """Публичный профиль — без чувствительных данных"""
    id: uuid.UUID
    first_name: str | None
    last_name: str | None
    avatar_key: str | None
    is_seller: bool
    seller_profile: SellerProfileRead | None = None

    model_config = ConfigDict(from_attributes=True)
