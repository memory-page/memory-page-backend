from typing import cast
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, exceptions
from fastapi import status
from pydantic import BaseModel, ValidationError

from app.base.settings import settings
from app.base.base_exception import BaseHTTPException


class Security:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return str(cls.pwd_context.hash(password))

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cast(bool, cls.pwd_context.verify(plain_password, hashed_password))


class JWT:
    class DecodedAccessToken(BaseModel):
        board_id: str
        exp: float

    @classmethod
    async def create_access_token(cls, data: dict[str, str]) -> str:

        to_encode = data.copy()

        KST = timezone(timedelta(hours=9))
        expire = datetime.now(KST) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire.timestamp()})

        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    
    @classmethod
    def decode_access_token(cls, token: str) -> DecodedAccessToken:
        try:
            decoded = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return cls.DecodedAccessToken.model_validate(decoded)
        except exceptions.ExpiredSignatureError:
            raise BaseHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 만료되었습니다.",
            )
        except exceptions.JWTError:
            raise BaseHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
            )
        except ValidationError:
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="토큰 데이터가 유효하지 않습니다.",
            )
