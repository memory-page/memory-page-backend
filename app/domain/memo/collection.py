import dataclasses
from typing import Any
from bson import ObjectId

from app.db.database import db
from app.domain.memo.document import MemoDocument


class MemoCollection:
    _collection = db["memo"]

    @classmethod
    def _parse(cls, document: dict[str, Any]) -> MemoDocument:
        return MemoDocument(
            _id=document["_id"],
            board_id=document["board_id"],
            locate_idx=document["locate_idx"],
            bg_num=document["bg_num"],
            author=document["author"],
            content=document["content"],
        )

    @classmethod
    async def insert_memo(cls, document: MemoDocument) -> str:
        """
        메모를 생성하는 함수

        Parameters
        ---
        document: MemoDocument, 생성할 메모 데이터 객체

        Return
        ---
        str, 생성된 메모의 ID
        """
        insert_document = dataclasses.asdict(document)
        result = await cls._collection.insert_one(document=insert_document)

        return str(result.inserted_id)
    
    @classmethod
    async def find_memo_by_id(cls, memo_id: str) -> MemoDocument | None:
        """
        메모 ID를 사용해 메모를 조회하는 함수

        Parameters
        ---
        memo_id: str, 조회할 메모의 ID

        Return
        ---
        MemoDocument | None
        """
        result = await cls._collection.find_one(filter={"_id": ObjectId(memo_id)})

        return cls._parse(result) if result else None
