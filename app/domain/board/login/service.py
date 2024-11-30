from fastapi import status
from typing import Any

from app.domain.board.service import BoardService
from app.domain.board.collection import BoardCollection
from app.domain.board.document import BoardDocument
from app.domain.board.login.request import LoginRequest
from app.base.base_exception import BaseHTTPException
from app.utils.security import verify_password
from app.utils.jwt import create_access_token


class BoardLoginService(BoardService):
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
