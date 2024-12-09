from pydantic import BaseModel, Field


class MemoInsertRequest(BaseModel):
    locate_idx: int = Field(..., description="메모 위치", examples=[0])
    bg_num: int = Field(..., description="배경 번호", examples=[0])
    author: str = Field(..., description="작성자", examples=["민서"])
    content: str = Field(
        ..., description="메모 내용", examples=["너는 좋은 개발자가 되렴"]
    )
