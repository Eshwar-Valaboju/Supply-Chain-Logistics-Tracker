import motor.motor_asyncio
from .config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)

def get_database():
    return client[settings.mongo_db_name]

def get_collection(name: str):
    return get_database()[name]
