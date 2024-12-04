from fastapi import APIRouter

from app.domain.board.request import (
    BoardInsertRequest,
    LoginRequest,
    BoardValidateRequest,
)
from app.domain.board.response import (
    BoardInsertData,
    BoardInsertResponse,
    LogintData,
    LoginResponse,
    BoardValidateData,
    BoardValidateResponse,
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


@router.post("/board/validate", response_model=BoardValidateResponse)
async def board_name_validate(request: BoardValidateRequest) -> BoardValidateResponse:
    result_bool = await BoardService.board_name_validate(request=request)

    response_data = BoardValidateData(is_pass=result_bool)
    return BoardValidateResponse(
        detail="칠판 이름, 비밀번호 검증 성공", data=response_data
    )
