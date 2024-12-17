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
    BoardGetData,
    BoardGetResponse,
)
from app.domain.board.service import BoardService
from app.domain.memo.request import MemoInsertRequest
from app.domain.memo.response import MemoInsertData, MemoInsertResponse
from app.domain.memo.service import MemoService
from app.core.exception import *
from app.utils.responses_creater import ResponsesCreater
from app.core.swagger_responses import *

router = APIRouter()
response_creater = ResponsesCreater()


@router.post(
    path="/board",
    response_model=BoardInsertResponse,
    responses=post_board_responses(),
)
async def board_insert(request: BoardInsertRequest) -> BoardInsertResponse:
    insertd_id = await BoardService.insert_board(request=request)

    response_data = BoardInsertData(board_id=insertd_id)
    return BoardInsertResponse(detail="칠판 생성 완료.", data=response_data)


@router.post(
    "/board/login", response_model=LoginResponse, responses=post_board_responses()
)
async def login(request: LoginRequest) -> LoginResponse:
    board_id, access_token = await BoardService.login(request)

    response_data = LogintData(board_id=board_id, access_token=access_token)
    return LoginResponse(detail="로그인 완료", data=response_data)


@router.post(
    "/board/validate",
    response_model=BoardValidateResponse,
    responses=post_board_validate_responses(),
)
async def board_name_validate(request: BoardValidateRequest) -> BoardValidateResponse:
    result_bool = await BoardService.board_name_validate(request=request)

    response_data = BoardValidateData(is_pass=result_bool)
    return BoardValidateResponse(
        detail="칠판 이름, 비밀번호 검증 성공", data=response_data
    )


@router.post(
    path="/board/{board_id}/memo/",
    response_model=MemoInsertResponse,
    responses=post_board_boardid_memo_responses(),
)
async def memo_insert(board_id: str, request: MemoInsertRequest) -> MemoInsertResponse:
    inserted_id = await MemoService.insert_memo(board_id=board_id, request=request)

    response_data = MemoInsertData(memo_id=inserted_id)
    return MemoInsertResponse(detail="메모지 생성 완료.", data=response_data)


@router.get(
    path="/board/{board_id}/",
    response_model=BoardGetResponse,
    responses=get_board_boardid_responses(),
)
async def board_get(board_id: str) -> BoardGetResponse:
    bg_num, memo_list = await BoardService.get_board(board_id=board_id)

    response_data = BoardGetData(bg_num=bg_num, memo_list=memo_list)
    return BoardGetResponse(detail="칠판 조회.", data=response_data)
