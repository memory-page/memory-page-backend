import dataclasses

from app.base.base_document import BaseDocument


@dataclasses.dataclass(kw_only=True, frozen=True)
class MemoDocument(BaseDocument):
    board_id: str
    locate_idx: int
    bg_num: int
    author: str
    content: str
