from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import secrets
from app_.models import User
from app_.database import get_session as get_core_session

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expiry = datetime.now() + timedelta(minutes=expires_minutes)
    to_encode["exp"] = expiry
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_core_session)
):
    if creds is None:
        raise HTTPException(status_code=401, detail="Missing token")

    token = creds.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.exec(select(User).where(User.id == user_id))
    user = result.first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

