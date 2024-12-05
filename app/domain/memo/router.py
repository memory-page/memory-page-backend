from fastapi import APIRouter, Depends

from app.domain.memo.response import (
    MemoResponse,
    MemoData,
)
from app.domain.memo.service import MemoService
from app.utils.security import JWT

router = APIRouter()


@router.get(path="/memo/{memo_id}", response_model=MemoResponse)
async def memo_get(
    memo_id: str, token: JWT.Payload = Depends(JWT.decode_access_token)
) -> MemoResponse:
    author, content = await MemoService.get_memo(memo_id=memo_id, token=token)

    response_data = MemoData(author=author, content=content)
    return MemoResponse(detail="메모지 조회.", data=response_data)
