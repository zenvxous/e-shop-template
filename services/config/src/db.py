from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings

settings = get_settings()

client = AsyncIOMotorClient(settings.mongo_url)
database = client.get_default_database()


def get_configs_collection():
    return database.configs
