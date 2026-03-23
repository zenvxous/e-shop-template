from fastapi import APIRouter, UploadFile, File, HTTPException

from .models import (
    MarketplaceConfig,
    MarketplaceConfigUpdate,
    CheckoutConfig,
    CheckoutConfigUpdate,
    FeaturesConfig,
    FeaturesConfigUpdate,
    LogoUploadResponse
)
from .services import ConfigService

router = APIRouter(prefix="/config", tags=["config"])
config_service = ConfigService()


@router.get("/marketplace", response_model=MarketplaceConfig)
async def get_marketplace_config():
    """Get marketplace configuration."""
    return await config_service.get_marketplace_config()


@router.patch("/marketplace", response_model=MarketplaceConfig)
async def update_marketplace_config(update: MarketplaceConfigUpdate):
    """Update marketplace configuration."""
    return await config_service.update_marketplace_config(update)


@router.get("/checkout", response_model=CheckoutConfig)
async def get_checkout_config():
    """Get checkout configuration."""
    return await config_service.get_checkout_config()


@router.patch("/checkout", response_model=CheckoutConfig)
async def update_checkout_config(update: CheckoutConfigUpdate):
    """Update checkout configuration."""
    return await config_service.update_checkout_config(update)


@router.get("/features", response_model=FeaturesConfig)
async def get_features_config():
    """Get features configuration."""
    return await config_service.get_features_config()


@router.patch("/features", response_model=FeaturesConfig)
async def update_features_config(update: FeaturesConfigUpdate):
    """Update features configuration."""
    return await config_service.update_features_config(update)


@router.post("/logo", response_model=LogoUploadResponse)
async def upload_logo(file: UploadFile = File(...)):
    """Upload marketplace logo to MinIO storage."""
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Validate file size (max 5MB)
    if file.size and file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be less than 5MB")
    
    try:
        # Read file content
        file_data = await file.read()
        
        # Upload to MinIO
        result = await config_service.upload_logo(
            file_data=file_data,
            content_type=file.content_type,
            filename=file.filename or "logo.png"
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload logo: {str(e)}")
