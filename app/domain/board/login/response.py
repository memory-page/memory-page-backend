from pydantic import BaseModel

from app.base.base_response import BaseResponseModel


class LogintData(BaseModel):
    board_id: str
    access_token: str


class LoginResponse(BaseResponseModel):
    data: LogintData
