from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.mongo_db_name]
user_collection = database.get_collection("users")  