import uuid

from fastapi import APIRouter, Depends, UploadFile, File, status

from src.dep import get_user_service, get_minio
from src.schemas.user import (
    UserCreate, UserRead, UserUpdate, UserPublicRead,
    BecomeSellerRequest, SellerProfileUpdate,
)
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


# ──────────── Sync с Keycloak ────────────

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """Вызывается при регистрации через Keycloak"""
    return await service.create(data)


# ──────────── Публичные профили ────────────

@router.get("/public/{user_id}", response_model=UserPublicRead)
async def get_public_profile(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    """Публичный профиль (для других пользователей)"""
    return await service.get_public(user_id)


# ──────────── Профиль конкретного пользователя ────────────

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    return await service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    return await service.update(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    await service.deactivate(user_id)


# ──────────── Аватар ────────────

@router.post("/{user_id}/avatar", response_model=UserRead)
async def upload_avatar(
    user_id: uuid.UUID,
    file: UploadFile = File(...),
    service: UserService = Depends(get_user_service),
    minio=Depends(get_minio),
):
    return await service.upload_avatar(user_id, file, minio)


# ──────────── Seller ────────────

@router.post("/{user_id}/become-seller", response_model=UserRead)
async def become_seller(
    user_id: uuid.UUID,
    data: BecomeSellerRequest,
    service: UserService = Depends(get_user_service),
):
    return await service.become_seller(user_id, data)


@router.patch("/{user_id}/seller-profile", response_model=UserRead)
async def update_seller_profile(
    user_id: uuid.UUID,
    data: SellerProfileUpdate,
    service: UserService = Depends(get_user_service),
):
    return await service.update_seller_profile(user_id, data)
