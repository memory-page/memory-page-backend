import dataclasses
from httpx import AsyncClient, ASGITransport, Response
from typing import Tuple

from app.main import app


@dataclasses.dataclass(kw_only=True, frozen=True)
class login_dto:
    board_id: str
    access_token: str

async def mock_login(
    board_name: str, 
    password: str
) -> Tuple[Response, login_dto]:
    login_request = {
        "board_name":board_name,
        "password":password
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/login", json=login_request)
    return response
