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


class MemoSummaryData(BaseModel):
    memo_id: str = Field(..., description="메모 아이디", examples=["uuid"])
    locate_idx: int = Field(..., description="메모 위치", examples=[0])
    bg_num: int = Field(..., description="배경 번호", examples=[0])


class MemoValidateData(BaseModel):
    is_pass: bool = Field(
        ..., description="메모 검증 통과 여부", examples=[True, False]
    )


class MemoValidateResponse(BaseResponseModel):
    data: MemoValidateData
