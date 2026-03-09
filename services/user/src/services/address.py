import uuid
from fastapi import HTTPException

from src.repo.address import AddressRepository
from src.schemas.address import AddressCreate, AddressRead, AddressUpdate


class AddressService:
    def __init__(self, repo: AddressRepository):
        self.repo = repo

    async def create(
        self, user_id: uuid.UUID, data: AddressCreate
    ) -> AddressRead:
        address = await self.repo.create(user_id, data)
        return AddressRead.model_validate(address)

    async def get_all(self, user_id: uuid.UUID) -> list[AddressRead]:
        addresses = await self.repo.get_by_user(user_id)
        return [AddressRead.model_validate(a) for a in addresses]

    async def get(
        self, user_id: uuid.UUID, address_id: uuid.UUID
    ) -> AddressRead:
        address = await self._get_owned(user_id, address_id)
        return AddressRead.model_validate(address)

    async def update(
        self,
        user_id: uuid.UUID,
        address_id: uuid.UUID,
        data: AddressUpdate,
    ) -> AddressRead:
        address = await self._get_owned(user_id, address_id)
        address = await self.repo.update(address, data)
        return AddressRead.model_validate(address)

    async def set_default(
        self, user_id: uuid.UUID, address_id: uuid.UUID
    ) -> AddressRead:
        address = await self._get_owned(user_id, address_id)
        address = await self.repo.set_default(address)
        return AddressRead.model_validate(address)

    async def delete(
        self, user_id: uuid.UUID, address_id: uuid.UUID
    ) -> None:
        address = await self._get_owned(user_id, address_id)
        await self.repo.delete(address)

    async def _get_owned(
        self, user_id: uuid.UUID, address_id: uuid.UUID
    ):
        """Получить адрес и проверить, что он принадлежит пользователю"""
        address = await self.repo.get_by_id(address_id)
        if not address or address.user_id != user_id:
            raise HTTPException(status_code=404, detail="Address not found")
        return address
