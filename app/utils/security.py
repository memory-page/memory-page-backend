from typing import cast
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.base.settings import settings


class Security:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return str(cls.pwd_context.hash(password))

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cast(bool, cls.pwd_context.verify(plain_password, hashed_password))
    
    
class JWT:
    @classmethod
    async def create_access_token(cls, data: dict[str, str]) -> str:

        to_encode = data.copy()

        KST = timezone(timedelta(hours=9))
        expire = datetime.now(KST) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire.timestamp()})

        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    