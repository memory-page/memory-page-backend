import re
from typing import Optional
from korcen import korcen
from datetime import datetime, timedelta, timezone

from app.domain.board.request import (
    BoardInsertRequest,
    LoginRequest,
    BoardValidateRequest,
)
from app.domain.board.collection import BoardCollection
from app.domain.board.document import BoardDocument
from app.utils.security import Security, JWT
from app.core.exception import (
    BoardGraduatedException,
    CanNotUseBadWordInNameException,
    CanNotUseSpaceFrontEndBackInNameException,
    CanNotUseSpaceInPasswordException,
    DoesNotExistBoardException,
    DuplicateNameException,
    MinLengthInPasswordException,
    OnlyKrEngNumSpecialInNameException,
    TooLongNameException,
    TooShortNameException,
    ValidateDateStrException,
    WrongNameOrPasswordInValidateLoginException,
)
from app.domain.memo.response import MemoSummaryData
from app.domain.memo.collection import MemoCollection


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

        graduated_at = await cls._validate_date_str(request.graduated_at)

        insert_board = BoardDocument(
            board_name=request.board_name,
            password=await Security.hash_password(request.password),
            bg_num=request.bg_num,
            graduated_at=graduated_at,
        )

        inserted_id = await BoardCollection.insert_board(document=insert_board)
        return inserted_id

    @classmethod
    async def get_board(
        cls, board_id: str, token: Optional[JWT.Payload] = None
    ) -> tuple[bool, str, int, list[MemoSummaryData]]:
        """
        칠판 정보를 가져오는 함수

        Parameters
        ---
        board_id: str, 요청된 칠판 ID

        Return
        ---
        tuple[int, list[MemoSummaryData]], 칠판 배경 번호와 메모 리스트
        """
        is_self = False

        if token:
            if await cls._validate_board_id_in_token(
                board_id=board_id, token_board_id=token.board_id
            ):
                is_self = True

        await cls._validate_object_id(board_id=board_id)
        board = await cls._validate_board_id(board_id=board_id)
        memo_list = await cls.get_memo_list_by_board_id(board_id=board_id)

        return is_self, board.board_name, board.bg_num, memo_list

    @classmethod
    async def get_memo_list_by_board_id(cls, board_id: str) -> list[MemoSummaryData]:
        """
        메모 리스트를 반환하는 함수

        Parameters
        ---
        board_id: str, 메모가 속한 칠판 ID

        Return
        ---
        list[MemoSummaryData], 메모 요약 리스트
        """
        memo_list = await MemoCollection.find_memo_list_by_board_id(board_id=board_id)
        memo_summary_list = [
            MemoSummaryData(
                memo_id=str(memo._id), locate_idx=memo.locate_idx, bg_num=memo.bg_num
            )
            for memo in memo_list
        ]
        return memo_summary_list

    @classmethod
    async def login(cls, request: LoginRequest) -> tuple[str, str]:
        """
        로그인 처리하는 함수

        Parameter
        ---
        request: LoginRequest, 로그인 요청 정보

        Return
        ---
        dict, 로그인 응답 데이터 (딕셔너리 형태로 반환)
        """
        await cls._validate_password(password=request.password)

        board = await cls._validate_login(request.board_name, request.password)

        board_id = str(board._id)
        access_token = await JWT.create_access_token(board_id)
        return board_id, access_token

    @classmethod
    async def _length_checker(cls, board_name: str) -> None:
        max_len = 16 if re.match(r"^[a-zA-Z]+$", board_name) else 8
        if not 2 <= len(board_name):
            raise TooShortNameException()
        elif not len(board_name) <= max_len:
            raise TooLongNameException()

    @classmethod
    async def _validate_board_name(cls, board_name: str) -> bool:
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
        : bool, 검사 통과 표시

        Exception
        ---
        400: 중복된 이름이 존재합니다.
        400: 이름이 너무 짧습니다.
        400: 이름이 너무 깁니다.
        400: 이름의 앞과 뒤는 공백일 수 없습니다.
        400: 이름은 한글, 영어, 숫자, 특수문자만 사용할 수 있습니다.
        400: 이름에 비속어는 사용할 수 없습니다.
        """
        # 중복 이름 금지
        result = await BoardCollection.find_board_by_name(board_name=board_name)
        if result is not None:
            raise DuplicateNameException()

        # 최소 2자 ~ 최대(한글 8자, 영어 16자, 혼용일 경우 8자)
        await cls._length_checker(board_name=board_name)

        # 앞 뒤 공백 금지
        if board_name[0] == " " or board_name[-1] == " ":
            raise CanNotUseSpaceFrontEndBackInNameException()

        # 한글, 영어, 숫자, 특수문자만 허용
        if not re.match(
            r"^[가-힣a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`]+$", board_name
        ):
            raise OnlyKrEngNumSpecialInNameException()

        # 비속어 금지, Reference: https://github.com/Tanat05/korcen
        if korcen.check(board_name):
            raise CanNotUseBadWordInNameException()

        return True

    @classmethod
    async def _validate_password(cls, password: str) -> bool:
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
        : bool, 검사 통과 여부

        Exception
        ---
        400: 비밀번호는 띄어쓰기를 사용할 수 없습니다.
        400: 비밀번호는 영어, 숫자, 특수문자만 사용 가능합니다.
        400: 비밀번호는 최소 4자 이상이어야 합니다.
        """

        # 띄어쓰기 사용 금지
        if " " in password:
            raise CanNotUseSpaceInPasswordException()

        # 영어, 숫자, 특수문자만 허용
        if not re.fullmatch(
            r"^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`]+$", password
        ):
            raise CanNotUseSpaceInPasswordException()

        # 최소 4자 이상
        if len(password) < 4:
            raise MinLengthInPasswordException()

        return True

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
            raise WrongNameOrPasswordInValidateLoginException()

        if not await Security.verify_password(password, board.password):
            raise WrongNameOrPasswordInValidateLoginException()

        return board

    @classmethod
    async def board_name_validate(cls, request: BoardValidateRequest) -> bool:
        """
        유저 이름 검증하는 함수

        Parameter
        ---
        board_name: str, 보드 이름

        Return
        ---
        : bool, 이름 검증 성공 여부(성공시 True 반환, 실패시 에러 발생)

        Exception
        ---
        None
        """
        name_validate_result = await cls._validate_board_name(
            board_name=request.board_name
        )
        password_validate_result = await cls._validate_password(
            password=request.password
        )

        return name_validate_result is True and password_validate_result is True

    @classmethod
    async def _validate_date_str(cls, date_str: str) -> datetime:
        """
        문자열을 datetime 객체로 바꿔주는 함수

        Parameter
        ---
        date_str: str, 문자열 객체(yyyy-mm-dd 형식이어야 함)

        Return
        ---
        date_time: datetime, datetime 객체

        Exception
        ---
        400: 날짜 문자열의 형식이 올바르지 않습니다.
        """
        try:
            date_time = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidateDateStrException()

        return date_time

    @classmethod
    async def _validate_board_id(cls, board_id: str) -> BoardDocument:
        """
        board_id의 존재 여부를 검증하는 함수

        Parameters
        ---
        board_id: str, 검증할 칠판 ID

        Return
        ---
        BoardDocument, 존재하는 경우 칠판 문서 객체

        Exceptions
        ---
        404: board_id에 해당하는 칠판이 존재하지 않을 경우
        """
        board = await BoardCollection.find_board_by_id(board_id=board_id)
        if board is None:
            raise DoesNotExistBoardException()
        return board

    @classmethod
    async def _validate_board_id_in_token(
        cls, board_id: str, token_board_id: str
    ) -> bool:
        """
        토큰에 포함된 칠판 ID가 제공된 칠판 ID와 일치하는지 검증하는 함수

        Parameters
        ---
        board_id: str, 검증할 칠판 ID
        token_board_id: str, 토큰에서 추출된 칠판 ID

        Exceptions
        ---
        400: 칠판 ID가 토큰의 칠판 ID와 일치하지 않을 경우
        """

        if board_id != token_board_id:
            return False
        return True

    @classmethod
    async def _validate_object_id(cls, board_id: str) -> None:
        """
        board_id가 ObjectId형식인지 검증하는 함수

        Parameters
        ---
        board_id: str, 검증할 칠판 ID

        Exceptions
        ---
        400: board_id가 24자가 아니거나 유효한 16진수가 아닐 경우
        """
        if len(board_id) != 24 or not all(
            c in "0123456789abcdefABCDEF" for c in board_id
        ):
            raise DoesNotExistBoardException()

    @classmethod
    async def _validate_board_graduation(cls, board_id: str) -> None:
        """
        칠판의 graduated_at보다 이전인지 확인하는 함수

        Parameters
        ---
        board_id: str, 검증할 칠판 ID

        Exceptions
        ---
        403: 조회 시점이 졸업 시점보다 이전일 경우
        """
        KST = timezone(timedelta(hours=9))
        board = await cls._validate_board_id(board_id=board_id)
        korea_time = datetime.now(KST)
        graduated_at = board.graduated_at.astimezone(KST)
        if korea_time < graduated_at:
            raise BoardGraduatedException()
