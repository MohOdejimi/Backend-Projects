import bcrypt 
import datetime
import jwt

from config import settings

def hashPassword(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verifyPassword(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
                    )

def generate_token(email: str) -> str:
    expires_delta = datetime.timedelta(minutes=settings.access_token_expire_minutes)
    expire_at = datetime.datetime.now(datetime.UTC) + expires_delta

    payload = {
        "sub": email, 
        "exp": expire_at
    }
    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")

    return {
        "access_token": token,
        "expires_in": int(expires_delta.total_seconds()),
    }

