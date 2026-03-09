import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AddressCreate(BaseModel):
    label: str | None = None
    country: str
    city: str
    street: str
    building: str
    apartment: str | None = None
    postal_code: str
    is_default: bool = False


class AddressUpdate(BaseModel):
    label: str | None = None
    country: str | None = None
    city: str | None = None
    street: str | None = None
    building: str | None = None
    apartment: str | None = None
    postal_code: str | None = None
    is_default: bool | None = None


class AddressRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    label: str | None
    country: str
    city: str
    street: str
    building: str
    apartment: str | None
    postal_code: str
    is_default: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
