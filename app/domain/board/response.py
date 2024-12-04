from pydantic import BaseModel

from app.base.base_response import BaseResponseModel


class BoardInsertData(BaseModel):
    board_id: str


class BoardInsertResponse(BaseResponseModel):
    data: BoardInsertData


class LogintData(BaseModel):
    board_id: str
    access_token: str


class LoginResponse(BaseResponseModel):
    data: LogintData


class BoardValidateData(BaseModel):
    is_pass: bool


class BoardValidateResponse(BaseResponseModel):
    data: BoardValidateData
