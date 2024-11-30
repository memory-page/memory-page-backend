from fastapi import APIRouter

from app.domain.board.request import BoardInsertRequest
from app.domain.board.response import (
    BoardInsertData,
    BoardInsertResponse
)
from app.domain.board.service import BoardService

router = APIRouter()


@router.post(path="/board", response_model=BoardInsertResponse)
async def board_insert(request: BoardInsertRequest) -> BoardInsertResponse:
    insertd_id = await BoardService.insert_board(request=request)

    response_data = BoardInsertData(board_id=insertd_id)
    return BoardInsertResponse(detail="칠판 생성 완료.", data=response_data)
