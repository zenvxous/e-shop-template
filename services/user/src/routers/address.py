import uuid

from fastapi import APIRouter, Depends, status

from src.dep import get_address_service
from src.schemas.address import AddressCreate, AddressRead, AddressUpdate
from src.services.address import AddressService

router = APIRouter(prefix="/users/{user_id}/addresses", tags=["Addresses"])


@router.get("/", response_model=list[AddressRead])
async def list_addresses(
    user_id: uuid.UUID,
    service: AddressService = Depends(get_address_service),
):
    return await service.get_all(user_id)


@router.post("/", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
async def create_address(
    user_id: uuid.UUID,
    data: AddressCreate,
    service: AddressService = Depends(get_address_service),
):
    return await service.create(user_id, data)


@router.get("/{address_id}", response_model=AddressRead)
async def get_address(
    user_id: uuid.UUID,
    address_id: uuid.UUID,
    service: AddressService = Depends(get_address_service),
):
    return await service.get(user_id, address_id)


@router.patch("/{address_id}", response_model=AddressRead)
async def update_address(
    user_id: uuid.UUID,
    address_id: uuid.UUID,
    data: AddressUpdate,
    service: AddressService = Depends(get_address_service),
):
    return await service.update(user_id, address_id, data)


@router.post("/{address_id}/set-default", response_model=AddressRead)
async def set_default_address(
    user_id: uuid.UUID,
    address_id: uuid.UUID,
    service: AddressService = Depends(get_address_service),
):
    return await service.set_default(user_id, address_id)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    user_id: uuid.UUID,
    address_id: uuid.UUID,
    service: AddressService = Depends(get_address_service),
):
    await service.delete(user_id, address_id)
