from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"


# 환경 설정을 인스턴스로 가져오기
settings = Settings()  # type: ignore
