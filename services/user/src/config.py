from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "user-service"
    port: int = 8001
    log_level: str = "INFO"
    debug: bool = False

    database_url: str

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "marketplace"
    rabbitmq_pass: str = ""

    keycloak_url: str = "http://keycloak:8080"
    keycloak_realm: str = "ecommerce"
    keycloak_client_id: str = "user-service"
    keycloak_client_secret: str = ""

    minio_endpoint: str = "minio:9000"  # Без http:// для SDK
    minio_access_key: str = "minio"
    minio_secret_key: str = ""
    minio_bucket: str = "user-avatars"
    minio_use_ssl: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
