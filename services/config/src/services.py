import io
import uuid
from datetime import datetime
from typing import Optional

from miniopy_async import Minio
from .db import get_configs_collection
from .config import get_settings
from .models import (
    ConfigDocument,
    MarketplaceConfig,
    MarketplaceConfigUpdate,
    CheckoutConfig,
    CheckoutConfigUpdate,
    FeaturesConfig,
    FeaturesConfigUpdate,
    LogoUploadResponse
)


class ConfigService:
    def __init__(self):
        self.collection = get_configs_collection()
        settings = get_settings()
        
        # Initialize MinIO client
        self.minio_client = Minio(
            endpoint=settings.minio_endpoint.replace("http://", "").replace("https://", ""),
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False
        )
        self.minio_bucket = settings.minio_bucket
        
    async def ensure_bucket_exists(self):
        """Ensure MinIO bucket exists."""
        if not await self.minio_client.bucket_exists(self.minio_bucket):
            await self.minio_client.make_bucket(self.minio_bucket)

    async def upload_logo(self, file_data: bytes, content_type: str, filename: str) -> LogoUploadResponse:
        """Upload logo to MinIO and return URL."""
        await self.ensure_bucket_exists()
        
        # Generate unique filename
        file_extension = filename.split('.')[-1] if '.' in filename else 'png'
        object_name = f"logos/logo-{uuid.uuid4()}.{file_extension}"
        
        # Upload to MinIO
        file_stream = io.BytesIO(file_data)
        await self.minio_client.put_object(
            bucket_name=self.minio_bucket,
            object_name=object_name,
            data=file_stream,
            length=len(file_data),
            content_type=content_type
        )
        
        # Generate URL
        settings = get_settings()
        logo_url = f"{settings.minio_external_url}/{self.minio_bucket}/{object_name}"
        
        # Update marketplace config with new logo URL
        await self.update_marketplace_config(MarketplaceConfigUpdate(logo_url=logo_url))
        
        return LogoUploadResponse(
            logo_url=logo_url,
            message="Logo uploaded successfully"
        )

    async def get_config(self) -> Optional[ConfigDocument]:
        """Get the singleton config document."""
        doc = await self.collection.find_one({"_id": "singleton"})
        if doc:
            return ConfigDocument(**doc)
        return None

    async def create_default_config(self) -> ConfigDocument:
        """Create default config if none exists."""
        default_config = ConfigDocument(
            _id="singleton",
            marketplace=MarketplaceConfig(),
            checkout=CheckoutConfig(),
            features=FeaturesConfig()
        )
        await self.collection.update_one(
            {"_id": "singleton"},
            {"$set": default_config.model_dump(by_alias=True, exclude={"_id"})},
            upsert=True
        )
        return default_config

    async def get_or_create_config(self) -> ConfigDocument:
        """Get existing config or create default one."""
        config = await self.get_config()
        if not config:
            config = await self.create_default_config()
        return config

    async def get_marketplace_config(self) -> MarketplaceConfig:
        """Get marketplace configuration."""
        config = await self.get_or_create_config()
        return config.marketplace

    async def update_marketplace_config(self, update: MarketplaceConfigUpdate) -> MarketplaceConfig:
        """Update marketplace configuration."""
        config = await self.get_or_create_config()
        
        update_data = update.model_dump(exclude_unset=True)
        if update_data:
            for field, value in update_data.items():
                setattr(config.marketplace, field, value)
            
            await self.collection.update_one(
                {"_id": "singleton"},
                {
                    "$set": {
                        "marketplace": config.marketplace.model_dump(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        
        return config.marketplace

    async def get_checkout_config(self) -> CheckoutConfig:
        """Get checkout configuration."""
        config = await self.get_or_create_config()
        return config.checkout

    async def update_checkout_config(self, update: CheckoutConfigUpdate) -> CheckoutConfig:
        """Update checkout configuration."""
        config = await self.get_or_create_config()
        
        update_data = update.model_dump(exclude_unset=True)
        if update_data:
            for field, value in update_data.items():
                setattr(config.checkout, field, value)
            
            await self.collection.update_one(
                {"_id": "singleton"},
                {
                    "$set": {
                        "checkout": config.checkout.model_dump(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        
        return config.checkout

    async def get_features_config(self) -> FeaturesConfig:
        """Get features configuration."""
        config = await self.get_or_create_config()
        return config.features

    async def update_features_config(self, update: FeaturesConfigUpdate) -> FeaturesConfig:
        """Update features configuration."""
        config = await self.get_or_create_config()
        
        update_data = update.model_dump(exclude_unset=True)
        if update_data:
            for field, value in update_data.items():
                setattr(config.features, field, value)
            
            await self.collection.update_one(
                {"_id": "singleton"},
                {
                    "$set": {
                        "features": config.features.model_dump(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        
        return config.features
