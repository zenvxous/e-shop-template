import uuid
import io
from fastapi import HTTPException, UploadFile, status

from src.repo.user import UserRepository
from src.schemas.user import (
    UserCreate, UserRead, UserUpdate, UserPublicRead,
    BecomeSellerRequest, SellerProfileUpdate,
)
from src.config import get_settings

settings = get_settings()


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create(self, data: UserCreate) -> UserRead:
        if await self.repo.get_by_keycloak_id(data.keycloak_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )
        user = await self.repo.create(data)
        return UserRead.model_validate(user)

    async def get_by_id(self, user_id: uuid.UUID) -> UserRead:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user)

    async def get_by_keycloak_id(self, keycloak_id: str) -> UserRead:
        user = await self.repo.get_by_keycloak_id(keycloak_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user)

    async def get_public(self, user_id: uuid.UUID) -> UserPublicRead:
        user = await self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        return UserPublicRead.model_validate(user)

    async def update(self, user_id: uuid.UUID, data: UserUpdate) -> UserRead:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user = await self.repo.update(user, data)
        return UserRead.model_validate(user)

    async def upload_avatar(
        self,
        user_id: uuid.UUID,
        file: UploadFile,
        minio_client,
    ) -> UserRead:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Проверяем тип файла
        if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG or WebP images are allowed",
            )

        # Ключ в MinIO
        ext = file.filename.rsplit(".", 1)[-1] if file.filename else "jpg"
        object_key = f"avatars/{user_id}/{uuid.uuid4()}.{ext}"

        content = await file.read()
        await minio_client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=object_key,
            data=io.BytesIO(content),
            length=len(content),
            content_type=file.content_type,
        )

        user = await self.repo.set_avatar(user, object_key)
        return UserRead.model_validate(user)

    async def become_seller(
        self, user_id: uuid.UUID, data: BecomeSellerRequest
    ) -> UserRead:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_seller:
            raise HTTPException(
                status_code=409, detail="User is already a seller"
            )
        user = await self.repo.create_seller_profile(
            user, data.shop_name, data.description
        )
        return UserRead.model_validate(user)

    async def update_seller_profile(
        self, user_id: uuid.UUID, data: SellerProfileUpdate
    ) -> UserRead:
        user = await self.repo.get_by_id(user_id)
        if not user or not user.seller_profile:
            raise HTTPException(status_code=404, detail="Seller profile not found")
        await self.repo.update_seller_profile(
            user.seller_profile,
            data.shop_name,
            data.description,
        )
        user = await self.repo.get_by_id(user_id)
        return UserRead.model_validate(user)

    async def deactivate(self, user_id: uuid.UUID) -> None:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.repo.deactivate(user)
