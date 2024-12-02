from pydantic import BaseModel

from app.base.base_response import BaseResponseModel


class MemoInsertData(BaseModel):
    memo_id: str
    

class MemoInsertResponse(BaseResponseModel):
    data: MemoInsertData
