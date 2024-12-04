from fastapi import APIRouter, Depends

from app.domain.memo.request import MemoInsertRequest
from app.domain.memo.response import MemoInsertData, MemoInsertResponse, MemoResponse, MemoData
from app.domain.memo.service import MemoService
from app.utils.security import JWT

router = APIRouter()


@router.post(path="/{board_id}/memo/")
async def memo_insert(board_id: str, request: MemoInsertRequest) -> MemoInsertResponse:
    inserted_id = await MemoService.insert_memo(
        board_id=board_id,
        request=request
    )

    response_data = MemoInsertData(memo_id=inserted_id)
    return MemoInsertResponse(detail="메모지 생성 완료.", data=response_data)


@router.get(path="/memo/{memo_id}", response_model=MemoResponse)
async def memo_get(memo_id: str,  token: str = Depends(JWT.decode_access_token)) -> MemoResponse:
    author, content = await MemoService.get_memo(memo_id=memo_id, token=token)

    response_data = MemoData(author=author, content=content)
    return MemoResponse(detail="메모지 조회.", data=response_data)
