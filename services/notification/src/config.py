from pydantic_settings import BaseSettings
from fastapi_mail import ConnectionConfig
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # директория где лежит config.py

class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    TELEGRAM_BOT_TOKEN: str

    class Config:
        env_file = BASE_DIR / ".env"  # абсолютный путь к .env рядом с config.py

settings = Settings()

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)
