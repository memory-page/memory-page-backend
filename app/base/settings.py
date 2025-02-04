from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    MODE: str

    class Config:
        env_file = ".env"


# 환경 설정을 인스턴스로 가져오기
settings = Settings()  # type: ignore
