from pydantic import BaseModel


class BoardInsertRequest(BaseModel):
    board_name: str
    password: str
    bg_num: int
    graduated_at: str


class LoginRequest(BaseModel):
    board_name: str
    password: str


class BoardValidateRequest(BaseModel):
    board_name: str
    password: str
