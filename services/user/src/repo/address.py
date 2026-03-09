import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.address import Address
from src.schemas.address import AddressCreate, AddressUpdate


class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: uuid.UUID, data: AddressCreate) -> Address:
        # Если новый адрес default — сбрасываем флаг у остальных
        if data.is_default:
            await self._unset_default(user_id)

        address = Address(user_id=user_id, **data.model_dump())
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def get_by_id(self, address_id: uuid.UUID) -> Address | None:
        result = await self.session.execute(
            select(Address).where(Address.id == address_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: uuid.UUID) -> list[Address]:
        result = await self.session.execute(
            select(Address)
            .where(Address.user_id == user_id)
            .order_by(Address.is_default.desc(), Address.created_at.desc())
        )
        return list(result.scalars().all())

    async def update(
        self, address: Address, data: AddressUpdate
    ) -> Address:
        update_data = data.model_dump(exclude_unset=True)

        # Если меняем на default — сбрасываем у остальных
        if update_data.get("is_default"):
            await self._unset_default(address.user_id)

        for field, value in update_data.items():
            setattr(address, field, value)

        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def set_default(self, address: Address) -> Address:
        await self._unset_default(address.user_id)
        address.is_default = True
        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def delete(self, address: Address) -> None:
        await self.session.delete(address)
        await self.session.commit()

    async def _unset_default(self, user_id: uuid.UUID) -> None:
        """Снять флаг default со всех адресов пользователя"""
        await self.session.execute(
            update(Address)
            .where(Address.user_id == user_id, Address.is_default.is_(True))
            .values(is_default=False)
        )
