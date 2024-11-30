from datetime import datetime, timedelta, timezone
from jose import jwt

from app.base.settings import settings


def create_access_token(data: dict[str, str]) -> str:

    to_encode = data.copy()

    KST = timezone(timedelta(hours=9))

    expire = datetime.now(KST) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.isoformat()})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
