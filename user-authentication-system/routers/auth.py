import logging
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone 
from pymongo.errors import DuplicateKeyError 

from database import user_collection
from schema import UserCreate, UserOut 
from security import hashPassword

router = APIRouter(prefix='/auth', tags=["auth"])
logger = logging.getLogger(__name__)

@router.post('/register', response_model = UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate):
    user_doc = {
        "email": payload.email.lower(),
        "hashed_password": hashPassword(payload.password),
        "is_active": True,
        "is_verified": False, 
        "datetime": datetime.now(timezone.utc)
    }

    try:
        result = await user_collection.insert_one(user_doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exist"
        )
    except Exception:
        logger.exception("Unexpected error during user registration")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again"
        )

    return {
        "id": str(result.inserted_id),
        "email": user_doc["email"],
        "is_active": user_doc["is_active"],
        "is_verified": user_doc["is_verified"],
        "created_at": user_doc["datetime"]
    }
