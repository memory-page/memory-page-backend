from fastapi import APIRouter

from app.domain.board.login.request import LoginRequest
from app.domain.board.login.response import (
    LogintData,
    LoginResponse,
)
from app.domain.board.login.service import BoardLoginService

router = APIRouter()


@router.post("/board/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    board = await BoardLoginService.login(request)

    response_data = LogintData(
        board_id=board["board_id"], access_token=board["access_token"]
    )
    return LoginResponse(detail="로그인 완료", data=response_data)