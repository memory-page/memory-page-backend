from pydantic import BaseModel, Field

from app.base.base_response import BaseResponseModel


class BoardInsertData(BaseModel):
    board_id: str = Field(..., description="삽입된 보드 아이디", examples=["uuid"])


class BoardInsertResponse(BaseResponseModel):
    data: BoardInsertData


class LogintData(BaseModel):
    board_id: str = Field(..., description="칠판 아이디", examples=["uuid"])
    access_token: str = Field(..., description="엑세스 토큰", examples=["access token"])


class LoginResponse(BaseResponseModel):
    data: LogintData


class BoardValidateData(BaseModel):
    is_pass: bool = Field(
        ..., description="칠판 검증 통과 여부", examples=[True, False]
    )


class BoardValidateResponse(BaseResponseModel):
    data: BoardValidateData
