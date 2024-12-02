from pydantic import BaseModel
from datetime import datetime


class BoardInsertRequest(BaseModel):
    board_name: str
    password: str
    bg_num: int
    graduated_at: datetime


class LoginRequest(BaseModel):
    board_name: str
    password: str
    