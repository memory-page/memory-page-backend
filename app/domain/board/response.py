from pydantic import BaseModel, Field

from app.base.base_response import BaseResponseModel
from app.domain.memo.response import MemoSummaryData


class BoardInsertData(BaseModel):
    board_id: str = Field(..., description="삽입된 보드 아이디", examples=["uuid"])
    access_token: str = Field(..., description="엑세스 토큰", examples=["access token"])


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


class BoardGetData(BaseModel):
    is_self: bool = Field(..., description="본인 조회 여부", examples=[True, False])
    board_name: str = Field(..., description="보드 이름", examples=["프로젝트 보드"])
    bg_num: int = Field(..., description="배경 번호", examples=[0])
    memo_list: list[MemoSummaryData] = Field(..., description="메모 리스트")


class BoardGetResponse(BaseResponseModel):
    data: BoardGetData
