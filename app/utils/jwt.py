from datetime import datetime, timedelta, timezone
from jose import jwt
from app.base.settings import settings


def create_access_token(data: dict[str, str]) -> str:

    to_encode = data.copy()

    KST = timezone(timedelta(hours=9))

    expire = datetime.now(KST) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.isoformat()})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
