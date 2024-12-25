from motor.motor_asyncio import AsyncIOMotorClient
from app.base.settings import settings

# MongoDB 클라이언트 설정
client = AsyncIOMotorClient(settings.DATABASE_URL)  # type: ignore

# 필요한 MongoDB 컬렉션을 가져옵니다
db = client["base"]
