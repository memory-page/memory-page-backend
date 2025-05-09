from korcen import korcen

from app.domain.memo.request import MemoInsertRequest
from app.domain.memo.collection import MemoCollection
from app.domain.memo.document import MemoDocument
from app.domain.board.service import BoardService
from app.utils.security import JWT
from app.core.exception import (
    CanNotUseBadWordInContentException,
    CanNotUseBadWordInNameException,
    CanNotUseSpaceFrontEndBackInNameException,
    ContentLengthException,
    DoesNotExistMemoException,
    NotEqualMemoIdAndBoardIdException,
    ValidateAuthorLengthException,
    SameLocateIdxMemoException,
)


class MemoService:
    @classmethod
    async def validate_memo(cls, author: str, content: str) -> bool:
        """
        메모 작성자와 내용을 검토하는 함수

        Parameters
        ---
        author: str, 메모 작성자
        content: str, 메모 내용

        Return
        ---
        bool(True), 이상이 없으면 Exception이 발생되지 않고 True 반환
        """
        await cls._validate_author(author=author)
        await cls._validate_content(content=content)

        return True

    @classmethod
    async def insert_memo(cls, board_id: str, request: MemoInsertRequest) -> str:
        """
        메모를 생성하는 서비스 함수

        Parameters
        ---
        board_id: str, 메모가 속한 칠판 ID
        request: MemoInsertRequest, 전달받은 메모 요청 데이터

        Return
        ---
        str, 생성된 메모의 ID
        """
        await BoardService._validate_object_id(board_id=board_id)
        await BoardService._validate_board_id(board_id=board_id)

        await cls._validate_author(author=request.author)
        await cls._validate_content(content=request.content)

        is_same = await MemoCollection.is_same_locate_idx_memo(
            board_id=board_id, locate_idx=request.locate_idx
        )

        if is_same:
            raise SameLocateIdxMemoException()

        insert_memo = MemoDocument(
            board_id=board_id,
            locate_idx=request.locate_idx,
            bg_num=request.bg_num,
            author=request.author,
            content=request.content,
        )

        inserted_id = await MemoCollection.insert_memo(document=insert_memo)
        return inserted_id

    @classmethod
    async def get_memo(cls, memo_id: str, token: JWT.Payload) -> tuple[str, str]:
        """
        메모 ID를 사용해 작성자와 내용을 조회하는 함수

        Parameters
        ---
        memo_id: str, 조회할 메모의 ID

        Return
        ---
        tuple[str, str], 메모의 작성자(author), 내용(content)
        """
        await cls._validate_object_id(memo_id=memo_id)
        memo = await cls._validate_memo_id(memo_id)
        await cls._validate_board_id_in_memo(
            memo_board_id=memo.board_id, token_board_id=token.board_id
        )
        await BoardService._validate_board_graduation(board_id=token.board_id)

        return memo.author, memo.content

    @classmethod
    async def _validate_content(cls, content: str) -> None:
        """
        메모 내용의 유효성을 검사하는 함수

        Parameters
        ---
        content: str, 검증할 메모 내용

        Return
        ---
        None

        Exceptions
        ---
        400: 내용에 비속어가 포함된 경우
        400: 내용의 길이가 1자 미만 100자 초과인 경우
        """
        # 비속어 금지, Reference: https://github.com/Tanat05/korcen
        if korcen.check(content):
            raise CanNotUseBadWordInContentException()

        # 내용 길이 검사 (임시로 길이 지정)
        if len(content) < 1 or len(content) > 100:
            raise ContentLengthException()

    @classmethod
    async def _validate_author(cls, author: str) -> None:
        """
        메모 작성자의 유효성을 검사하는 함수

        Parameters
        ---
        author: str, 검증할 작성자 이름

        Return
        ---
        None

        Exceptions
        ---
        400: 이름에 비속어가 포함된 경우
        400: 이름의 앞뒤에 공백이 있을 경우
        400: 이름의 길이가 1자 미만 10자 초과인 경우
        """
        # 비속어 금지, Reference: https://github.com/Tanat05/korcen
        if korcen.check(author):
            raise CanNotUseBadWordInNameException()

        # 앞 뒤 공백 금지
        if author[0] == " " or author[-1] == " ":
            raise CanNotUseSpaceFrontEndBackInNameException()

        # 이름 길이 검사 (임시로 길이 지정)
        if len(author) < 1 or len(author) > 10:
            raise ValidateAuthorLengthException()

    @classmethod
    async def _validate_memo_id(cls, memo_id: str) -> MemoDocument:
        """
        메모 ID의 유효성을 확인하고 해당 메모를 반환하는 함수

        Parameters
        ---
        memo_id: str, 확인할 메모의 ID

        Return
        ---
        MemoDocument, 유효한 메모 데이터 객체

        Exceptions
        ---
        404: 존재하지 않은 메모 ID일 경우
        """
        memo = await MemoCollection.find_memo_by_id(memo_id=memo_id)
        if not memo:
            raise DoesNotExistMemoException()

        return memo

    @classmethod
    async def _validate_board_id_in_memo(
        cls, memo_board_id: str, token_board_id: str
    ) -> None:
        """
        메모의 board_id와 JWT에서 추출한 board_id의 일치 여부를 검증하는 함수

        Parameters
        ---
        memo_board_id: str, 메모에 저장된 board_id
        token_board_id: str, JWT 토큰에서 추출한 board_id

        Return
        ---
        None

        Exceptions
        ---
        403: 메모의 board_id와 JWT의 board_id가 일치하지 않을 경우
        """
        if memo_board_id != token_board_id:
            raise NotEqualMemoIdAndBoardIdException()

    @classmethod
    async def _validate_object_id(cls, memo_id: str) -> None:
        """
        memo_id가 ObjectId형식인지 검증하는 함수

        Parameters
        ---
        memo_id: str, 검증할 메모 ID

        Exceptions
        ---
        400: memo_id가 24자가 아니거나 유효한 16진수가 아닐 경우
        """
        if len(memo_id) != 24 or not all(
            c in "0123456789abcdefABCDEF" for c in memo_id
        ):
            raise DoesNotExistMemoException()
