from pydantic import BaseModel, Field


class BoardInsertRequest(BaseModel):
    board_name: str = Field(..., description="생성할 칠판 이름", examples=["인규"])
    password: str = Field(..., description="비밀번호", examples=["password1"])
    bg_num: int = Field(..., description="배경 번호", examples=[0])
    graduated_at: str = Field(..., description="졸업 날짜", examples=["2025-02-12"])


class LoginRequest(BaseModel):
    board_name: str = Field(..., description="로그인할 칠판 이름", examples=["인규"])
    password: str = Field(..., description="비밀번호", examples=["password1"])


class BoardValidateRequest(BaseModel):
    board_name: str = Field(..., description="검증할 칠판 이름", examples=["인규"])
    password: str = Field(..., description="비밀번호", examples=["password1"])
