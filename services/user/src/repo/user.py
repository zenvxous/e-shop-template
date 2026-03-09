import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User, SellerProfile
from src.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_keycloak_id(self, keycloak_id: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.keycloak_id == keycloak_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def update(self, user: User, data: UserUpdate) -> User:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def set_avatar(self, user: User, avatar_key: str) -> User:
        user.avatar_key = avatar_key
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def deactivate(self, user: User) -> None:
        user.is_active = False
        await self.session.commit()

    async def create_seller_profile(
        self, user: User, shop_name: str, description: str | None
    ) -> User:
        profile = SellerProfile(
            user_id=user.id,
            shop_name=shop_name,
            description=description,
        )
        user.is_seller = True
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_seller_profile(
        self,
        profile: SellerProfile,
        shop_name: str | None,
        description: str | None,
    ) -> SellerProfile:
        if shop_name is not None:
            profile.shop_name = shop_name
        if description is not None:
            profile.description = description
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def verify_seller(self, profile: SellerProfile) -> SellerProfile:
        profile.is_verified = True
        await self.session.commit()
        await self.session.refresh(profile)
        return profile
