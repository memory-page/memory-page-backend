from fastapi import APIRouter

from app.domain.board.request import BoardInsertRequest, LoginRequest
from app.domain.board.response import (
    BoardInsertData,
    BoardInsertResponse,
    LogintData,
    LoginResponse,
)
from app.domain.board.service import BoardService

router = APIRouter()


@router.post(path="/board", response_model=BoardInsertResponse)
async def board_insert(request: BoardInsertRequest) -> BoardInsertResponse:
    insertd_id = await BoardService.insert_board(request=request)

    response_data = BoardInsertData(board_id=insertd_id)
    return BoardInsertResponse(detail="칠판 생성 완료.", data=response_data)


@router.post("/board/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    board_id, access_token = await BoardService.login(request)

    response_data = LogintData(board_id=board_id, access_token=access_token)
    return LoginResponse(detail="로그인 완료", data=response_data)
