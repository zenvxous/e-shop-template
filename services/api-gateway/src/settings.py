from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pydantic import Field

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOTENV = os.path.join(PROJECT_ROOT, ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    log_level: str = Field(default="DEBUG", alias="LOG_LEVEL")
    log_type: str = Field(default="dev", alias="LOG_TYPE")

settings = Settings()
