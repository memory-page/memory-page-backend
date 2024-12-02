from fastapi import status
import re
from korcen import korcen

from app.domain.board.request import BoardInsertRequest
from app.domain.board.collection import BoardCollection
from app.domain.board.document import BoardDocument
from app.base.base_exception import BaseHTTPException


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
            password=request.password,
            bg_num=request.bg_num,
            graduated_at=request.graduated_at,
        )

        inserted_id = await BoardCollection.insert_board(document=insert_board)
        return inserted_id

    @classmethod
    async def _length_checker(cls, board_name: str) -> None:
        max_len = 16 if re.match(r"^[a-zA-Z]+$", board_name) else 8
        if not 2 <= len(board_name):
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="이름이 너무 짧습니다."
            )
        elif not len(board_name) <= max_len:
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="이름이 너무 깁니다."
            )

    @classmethod
    async def _validate_board_name(cls, board_name: str) -> None:
        """
        칠판 이름 유효성 검사 함수

        조건
            - 중복 이름 금지
            - 최소 2자 ~ 최대(한글 8자, 영어 16자, 숫자 포함 혼용일 경우 8자)
            - 앞 뒤 공백 금지
            - 한글, 영어, 숫자, 특수문자만 허용
            - 비속어 금지

        Parameter
        ---
        board_name: str, 칠판 이름

        Return
        ---
        None

        Exception
        ---
        400: 중복된 이름이 존재합니다.
        400: 이름이 너무 짧습니다.
        400: 이름이 너무 깁니다.
        400: 이름의 앞과 뒤는 공백일 수 없습니다.
        400: 한글, 영어, 숫자, 특수문자만 사용할 수 있습니다.
        400: 이름에 비속어는 사용할 수 없습니다.
        """
        # 중복 이름 금지
        result = await BoardCollection.find_board_by_name(board_name=board_name)
        if result is not None:
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="중복된 이름이 존재합니다.",
            )

        # 최소 2자 ~ 최대(한글 8자, 영어 16자, 혼용일 경우 8자)
        await cls._length_checker(board_name=board_name)

        # 앞 뒤 공백 금지
        if board_name[0] == " " or board_name[-1] == " ":
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이름의 앞과 뒤는 공백일 수 없습니다.",
            )

        # 한글, 영어, 숫자, 특수문자만 허용
        if not re.match(
            r"^[가-힣a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`]+$", board_name
        ):
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="한글, 영어, 숫자, 특수문자만 사용할 수 있습니다.",
            )

        # 비속어 금지, Reference: https://github.com/Tanat05/korcen
        if korcen.check(board_name):
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이름에 비속어는 사용할 수 없습니다.",
            )

    @classmethod
    async def _validate_password(cls, password: str) -> None:
        """
        칠판 비밀번호 유효성 검사 함수

        조건
            - 띄어쓰기 금지
            - 영어, 숫자, 특수문자만 허용
            - 최소 4자 이상

        Parameter
        ---
        password: str, 비밀번호

        Return
        ---
        None

        Exception
        ---
        400: 비밀번호는 띄어쓰기를 사용할 수 없습니다.
        400: 비밀번호는 영어, 숫자, 특수문자만 사용 가능합니다.
        400: 비밀번호는 최소 4자 이상이어야 합니다.
        """

        # 띄어쓰기 사용 금지
        if " " in password:
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호에는 띄어쓰기를 사용할 수 없습니다.",
            )

        # 영어, 숫자, 특수문자만 허용
        if not re.fullmatch(
            r"^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`]+$", password
        ):
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호는 영어, 숫자, 특수문자만 사용할 수 있습니다.",
            )

        # 최소 4자 이상
        if len(password) < 4:
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호는 최소 4자 이상이어야 합니다.",
            )
