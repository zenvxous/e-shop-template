from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MarketplaceConfig(BaseModel):
    name: str = "My Shop"
    currency: str = "USD"
    primary_color: str = "#ff0000"
    logo_url: Optional[str] = None


class MarketplaceConfigUpdate(BaseModel):
    name: Optional[str] = None
    currency: Optional[str] = None
    primary_color: Optional[str] = None
    logo_url: Optional[str] = None


class LogoUploadResponse(BaseModel):
    logo_url: str
    message: str


class CheckoutConfig(BaseModel):
    require_phone: bool = True
    require_address: bool = True


class CheckoutConfigUpdate(BaseModel):
    require_phone: Optional[bool] = None
    require_address: Optional[bool] = None


class FeaturesConfig(BaseModel):
    reviews_enabled: bool = True
    promo_codes_enabled: bool = False


class FeaturesConfigUpdate(BaseModel):
    reviews_enabled: Optional[bool] = None
    promo_codes_enabled: Optional[bool] = None


class ConfigDocument(BaseModel):
    _id: str = "singleton"
    marketplace: MarketplaceConfig
    checkout: CheckoutConfig
    features: FeaturesConfig
    updated_at: datetime = Field(default_factory=datetime.utcnow)
