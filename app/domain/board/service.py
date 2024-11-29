from fastapi import status

from app.domain.board.request import BoardInsertRequest, LoginRequest
from app.domain.board.collection import BoardCollection
from app.domain.board.document import BoardDocument
from app.base.base_exception import BaseHTTPException
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token

from typing import Any


class BoardService:
    @classmethod
    async def insert_board(cls, request: BoardInsertRequest) -> str:
        """
        칠판 생성하는 함수

        Parameter
        ---
        request: BoardInsertRequest, 삽입하고자하는 칠판 요청

        Return
        ---
        str, 칠판 아이디
        """
        # 칠판 이름 유효성 확인
        await cls._validate_board_name(board_name=request.board_name)

        # 비밀번호 유효성 확인
        await cls._validate_password(password=request.password)

        insert_board = BoardDocument(
            board_name=request.board_name,
            password=hash_password(request.password),
            bg_num=request.bg_num,
            graduated_at=request.graduated_at,
        )

        inserted_id = await BoardCollection.insert_board(document=insert_board)
        return inserted_id

    @classmethod
    async def login(cls, request: LoginRequest) -> dict[str, Any]:
        """
        로그인 처리하는 함수

        Parameter
        ---
        request: LoginRequest, 로그인 요청 정보

        Return
        ---
        dict, 로그인 응답 데이터 (딕셔너리 형태로 반환)

        Exception
        ---
        401: 이름 또는 비밀번호가 올바르지 않습니다.
        """
        await cls._validate_password(password=request.password)

        board = await cls._validate_login(request.board_name, request.password)

        return {
            "board_id": str(board._id),
            "access_token": create_access_token(data={"board_id": str(board._id)}),
        }

    @classmethod
    async def _validate_board_name(cls, board_name: str) -> None:
        """
        칠판 이름 유효성 검사 함수
        1. 중복확인

        Parameter
        ---
        board_name: str, 칠판 이름

        Return
        ---
        None

        Exception
        ---
        409: 중복된 이름이 존재합니다.
        """
        # 중복확인
        result = await BoardCollection.find_board_by_name(board_name=board_name)
        if result is not None:
            raise BaseHTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="중복된 이름이 존재합니다."
            )

    @classmethod
    async def _validate_password(cls, password: str) -> None:
        """
        칠판 비밀번호 유효성 검사 함수
        1. 띄어쓰기 없는지 확인

        Parameter
        ---
        password: str, 비밀번호

        Return
        ---
        None

        Exception
        ---
        409: 비밀번호에는 띄어쓰기를 사용할 수 없습니다.
        """

        if " " in password:
            raise BaseHTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="비밀번호에는 띄어쓰기를 사용할 수 없습니다.",
            )

    @classmethod
    async def _validate_login(cls, board_name: str, password: str) -> BoardDocument:
        """
        로그인 가능 여부를 확인하는 함수
        - 보드 이름 유효성 확인
        - 비밀번호 유효성 확인

        Parameter
        ---
        board_name: str, 보드 이름
        password: str, 요청된 비밀번호

        Return
        ---
        BoardDocument, 보드 문서 객체

        Exception
        ---
        401: 보드 이름 또는 비밀번호가 올바르지 않으면 예외 발생
        """
        board = await BoardCollection.find_board_by_name(board_name)
        if not board:
            raise BaseHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이름 또는 비밀번호가 올바르지 않습니다.",
            )

        if not verify_password(password, board.password):
            raise BaseHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이름 또는 비밀번호가 올바르지 않습니다.",
            )

        return board
