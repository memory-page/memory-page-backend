from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        # 이곳에 환경변수를 직접 지정할 수 있습니다
        env_file = ".env"  # .env 파일을 사용하는 경우 (필수 아님)


# 환경 설정을 인스턴스로 가져오기
settings = Settings()
