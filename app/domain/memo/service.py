from fastapi import status
from korcen import korcen

from app.domain.memo.request import MemoInsertRequest
from app.domain.memo.collection import MemoCollection
from app.domain.memo.document import MemoDocument
from app.domain.board.service import BoardService
from app.base.base_exception import BaseHTTPException


class MemoService:
    @classmethod
    async def insert_memo(cls, board_id:str, request: MemoInsertRequest) -> str:
        """
        메모를 생성하는 서비스 함수

        Parameters
        ---
        board_id: str, 메모가 속한 칠판 ID
        request: MemoInsertRequest, 전달받은 메모 요청 데이터

        Return
        ---
        str, 생성된 메모의 ID
            
        Exceptions
        ---
        400: 게시판 ID가 유효하지 않을 경우
        400: 작성자 이름이 유효하지 않을 경우
        400: 메모 내용이 유효하지 않을 경우
        """
        await BoardService._validate_object_id(board_id=board_id)
        await BoardService._validate_board_id(board_id=board_id)
        
        await cls._validate_author(author=request.author)
        await cls._validate_content(content=request.content)

        insert_memo = MemoDocument(
            board_id=board_id,
            locate_idx=request.locate_idx,
            bg_num=request.bg_num,
            author=request.author,
            content=request.content
        )

        inserted_id = await MemoCollection.insert_memo(document=insert_memo)
        return inserted_id
    
    @classmethod
    async def get_memo(cls, memo_id: str, token: dict) -> tuple[str, str]:
        """
        메모 ID를 사용해 작성자와 내용을 조회하는 함수

        Parameters
        ---
        memo_id: str, 조회할 메모의 ID

        Return
        ---
        tuple[str, str], 메모의 작성자(author), 내용(content)
        """
        token_board_id = await cls._validate_token_board_id(token)
        await cls._validate_object_id(memo_id=memo_id)
        memo = await cls._validate_memo_id(memo_id)
        await cls._validate_board_id_in_memo(memo_board_id=memo.board_id, token_board_id=token_board_id)

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
        400: 내용의 길이가 1자 미만 30자 초과인 경우
        """
        # 비속어 금지, Reference: https://github.com/Tanat05/korcen
        if korcen.check(content):
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="내용에 비속어는 사용할 수 없습니다.",
            )
        
        # 내용 길이 검사 (임시로 길이 지정)
        if  len(content) < 1 or len(content) > 30:
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="내용은 1자 이상 30자 이하로 작성해야 합니다."
            )
            
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
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이름에 비속어는 사용할 수 없습니다.",
            )
            
        # 앞 뒤 공백 금지
        if author[0] == " " or author[-1] == " ":
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이름의 앞과 뒤는 공백일 수 없습니다.",
            )
            
        # 이름 길이 검사 (임시로 길이 지정)
        if len(author) < 1 or len(author) > 10:
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이름은 1자 이상 10자 이하로 작성해야 합니다."
            )
            
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
        401: 존재하지 않은 메모 ID일 경우
        """
        memo = await MemoCollection.find_memo_by_id(memo_id=memo_id)
        if not memo:
            raise BaseHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="존재하지 않은 메모입니다.",
            )
            
        return memo
    
    @classmethod
    async def _validate_board_id_in_memo(cls, memo_board_id: str, token_board_id: str) -> None:
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
            raise BaseHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="메모가 요청한 board_id에 속하지 않습니다.",
            )

    @classmethod
    async def _validate_token_board_id(cls, token: dict) -> str:
        """
        JWT에서 board_id를 추출하고 유효성을 검증하는 함수

        Parameters
        ---
        token: dict, 디코딩된 JWT 토큰

        Return
        ---
        str, JWT 토큰에서 추출한 board_id

        Exceptions
        ---
        401: JWT 토큰에서 board_id가 없거나 유효하지 않을 경우
        """
        token_board_id = token.get("board_id")
        if not token_board_id:
            raise BaseHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
            )
        return token_board_id
    
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
        if len(memo_id) != 24 or not all(c in '0123456789abcdefABCDEF' for c in memo_id):
            raise BaseHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="존재하지 않는 메모입니다.",
            )
