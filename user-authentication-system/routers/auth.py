import logging
from fastapi import APIRouter, Cookie, HTTPException, Response, status
from datetime import datetime, timezone 
from pymongo.errors import DuplicateKeyError 

from database import user_collection
from database.session_manager import create_session, get_user_session, delete_session
from schema import UserCreate, UserOut, UserLogin, UserToken 
from security import hashPassword, verifyPassword, generate_token

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

@router.post('/login', status_code=status.HTTP_200_OK)
async def log_user(payload: UserLogin, response: Response):
    email = payload.email.lower()
    password = payload.password 

    present = await user_collection.find_one({
        "email": email
    })

    if not present:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email/Password"
        )

    hashed_password = present['hashed_password'] 

    if not verifyPassword(password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email/Password"
        )

    """
    if not present['is_verified']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kindly check your email to acivate your account"
        )

    """
    token_data = generate_token(str(present["_id"]))

    session_id = await create_session(str(present["_id"]))
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        max_age=token_data["expires_in"],
    )

    return {
        "id": str(present["_id"]),
        "access_token": token_data["access_token"],
        "expires_in": token_data["expires_in"],
    }


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def log_user_out(
    response: Response,
    session_id: str | None = Cookie(default=None),
):
    if session_id:
        await delete_session(session_id)

    response.delete_cookie(key="session_id")


