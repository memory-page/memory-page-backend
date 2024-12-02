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
