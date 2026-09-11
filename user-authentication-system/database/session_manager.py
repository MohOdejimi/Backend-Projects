from itsdangerous import URLSafeSerializer
from database import session_collection 
from config import settings 

import datetime

secret_key = settings.secret_key
serializer = URLSafeSerializer(secret_key)

async def create_session(user_id: str): 
    session_id = serializer.dumps(
        {"user_id": user_id}
    )

    expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=settings.access_token_expire_minutes
    )

    await session_collection.insert_one({
        "user_id": user_id,
        "session_id": session_id,
        "expires_at": expires_at,
    })

    return session_id

async def get_user_session(session_id: str):
    session_info = await session_collection.find_one({"session_id": session_id})

    if session_info and session_info['expires_at'] > datetime.datetime.now(datetime.UTC):
        return session_info

    return None 

async def delete_session(session_id: str):
    await session_collection.delete_one({"session_id": session_id})
