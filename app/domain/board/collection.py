import dataclasses
from typing import Any

from app.db.database import db
from app.domain.board.document import BoardDocument


class BoardCollection:
    _collection = db["board"]

    @classmethod
    def _parse(cls, document: dict[str, Any]) -> BoardDocument:
        return BoardDocument(
            _id=document["_id"],
            board_name=document["board_name"],
            password=document["password"],
            bg_num=document["bg_num"],
            graduated_at=document["graduated_at"],
        )

    @classmethod
    async def insert_board(cls, document: BoardDocument) -> str:
        """
        칠판을 삽입하는 함수

        Parameter
        ---
        document: BoardDocument, 칠판 문서

        Return
        ---
        str, 삽입된 칠판 id
        """
        insert_document = dataclasses.asdict(document)
        result = await cls._collection.insert_one(document=insert_document)

        return str(result.inserted_id)

    @classmethod
    async def find_board_by_name(cls, board_name: str) -> BoardDocument | None:
        """
        칠판 이름으로 보드를 조회하는 함수

        Parameter
        ---
        board_name: str, 칠판 이름

        Return
        ---
        str, 삽입된 칠판 문서
        """
        result = await cls._collection.find_one(filter={"board_name": board_name})

        return cls._parse(result) if result else None
    
    @classmethod
    async def find_board_by_id(cls, board_id: int) -> BoardDocument | None:
        """
        칠판 아이디로 보드를 조회하는 함수

        Parameter
        ---
        board_id: int, 칠판 아이디

        Return
        ---
        삽입된 칠판 문서
        """
        result = await cls._collection.find_one(filter={"_id": board_id})

        return cls._parse(result) if result else None
