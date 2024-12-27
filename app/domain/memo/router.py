from fastapi import APIRouter, Path, Header

from app.domain.memo.request import MemoValidateRequest
from app.domain.memo.response import (
    MemoResponse,
    MemoData,
    MemoValidateData,
    MemoValidateResponse,
)
from app.domain.memo.service import MemoService
from app.utils.security import JWT
from app.core.swagger_responses import (
    get_memo_momoid_responses,
    get_memo_validate_responses,
)

router = APIRouter()


@router.get(
    path="/memo/{memo_id}",
    response_model=MemoResponse,
    responses=get_memo_momoid_responses(),
)
async def memo_get(
    memo_id: str = Path(..., description="메모 아이디", examples=["uuid"]),
    token: str = Header(..., description="토큰 값"),
) -> MemoResponse:
    author, content = await MemoService.get_memo(
        memo_id=memo_id, token=JWT.decode_access_token(token)
    )

    response_data = MemoData(author=author, content=content)
    return MemoResponse(detail="메모지 조회.", data=response_data)


@router.post(
    path="/memo/validate",
    response_model=MemoValidateResponse,
    responses=get_memo_validate_responses(),
)
async def memo_validate(request: MemoValidateRequest) -> MemoValidateResponse:
    is_pass = await MemoService.validate_memo(
        author=request.author, content=request.content
    )

    response_data = MemoValidateData(is_pass=is_pass)
    return MemoValidateResponse(detail="메모 검증 통과", data=response_data)
