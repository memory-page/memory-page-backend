from typing import cast
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, exceptions
from fastapi import status
from pydantic import BaseModel, ValidationError

from app.base.settings import settings
from app.core.exception import *


class Security:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return str(cls.pwd_context.hash(password))

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cast(bool, cls.pwd_context.verify(plain_password, hashed_password))


class JWT:
    class Payload(BaseModel):
        board_id: str
        exp: float

    @classmethod
    async def create_access_token(cls, board_id: str) -> str:

        KST = timezone(timedelta(hours=9))
        expire = datetime.now(KST) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode = cls.Payload(board_id=board_id, exp=expire.timestamp()).model_dump()

        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return cast(str, encoded_jwt)

    @classmethod
    def decode_access_token(cls, token: str) -> Payload:
        try:
            decoded = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return cls.Payload.model_validate(decoded)
        except exceptions.ExpiredSignatureError:
            raise ExpiredTokenException()
        except exceptions.JWTError:
            raise InvalidTokenException()
        except ValidationError:
            raise InvalidTokenDataException()
