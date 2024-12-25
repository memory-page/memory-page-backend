import dataclasses
from datetime import datetime

from app.base.base_document import BaseDocument


@dataclasses.dataclass(kw_only=True, frozen=True)
class BoardDocument(BaseDocument):
    board_name: str
    password: str
    bg_num: int
    graduated_at: datetime
