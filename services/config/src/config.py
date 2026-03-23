from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "config-service"
    log_level: str = "INFO"
    port: int = 8006
    
    mongo_url: str
    
    # MinIO settings
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str = "marketplace-assets"
    minio_external_url: str = "http://localhost:9000"
    
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
