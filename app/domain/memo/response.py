from pydantic import BaseModel, Field

from app.base.base_response import BaseResponseModel


class MemoInsertData(BaseModel):
    memo_id: str = Field(..., description="메모 아이디", examples=["uuid"])


class MemoInsertResponse(BaseResponseModel):
    data: MemoInsertData


class MemoData(BaseModel):
    author: str = Field(..., description="메모 작성자", examples=["민서"])
    content: str = Field(
        ..., description="메모 내용", examples=["너는 좋은 개발자가 되렴"]
    )


class MemoResponse(BaseResponseModel):
    data: MemoData
