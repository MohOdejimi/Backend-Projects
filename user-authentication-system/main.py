from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import client, user_collection
from routers.auth import router as auth_router

@asynccontextmanager
async def startup_db_check(app: FastAPI):
    try:
        await client.admin.command('ping')
        print('MongoDB Atlas Connected successfully')
        await user_collection.create_index("email", unique=True)
        yield
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas: {e}")
        raise


app = FastAPI(title="auth-service", lifespan=startup_db_check)
app.include_router(auth_router)