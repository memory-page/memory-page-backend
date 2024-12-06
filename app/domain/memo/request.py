from pydantic import BaseModel


class MemoInsertRequest(BaseModel):
    locate_idx: int
    bg_num: int
    author: str
    content: str
