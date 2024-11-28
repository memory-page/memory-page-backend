from pydantic import BaseModel

from app.base.base_response import BaseResponseModel


class BoardInsertData(BaseModel):
    board_id: str


class BoardInsertResponse(BaseResponseModel):
    data: BoardInsertData
