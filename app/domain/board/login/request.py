from pydantic import BaseModel


class LoginRequest(BaseModel):
    board_name: str
    password: str
