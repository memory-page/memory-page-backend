from fastapi import APIRouter

from app.domain.memo.request import MemoInsertRequest
from app.domain.memo.response import MemoInsertData, MemoInsertResponse
from app.domain.memo.service import MemoService

router = APIRouter()


@router.post(path="/{board_id}/memo/")
async def memo_insert(board_id: str, request: MemoInsertRequest) -> MemoInsertResponse:
    inserted_id = await MemoService.insert_memo(
        board_id=board_id,
        request=request
    )

    response_data = MemoInsertData(memo_id=inserted_id)
    return MemoInsertResponse(detail="메모지 생성 완료.", data=response_data)
