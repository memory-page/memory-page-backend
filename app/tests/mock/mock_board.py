from datetime import datetime, timedelta
import uuid
from httpx import AsyncClient, ASGITransport, Response
import dataclasses
from typing import Tuple

from app.main import app


@dataclasses.dataclass(kw_only=True, frozen=True)
class mock_board_dto:
    board_name: str
    password: str
    bg_num: int
    graduated_at: datetime


async def mock_create_board(
    board_name: str | None = None,
    password: str | None = None,
    bg_num: int = 0,
    graduated_at: datetime | None = None,
) -> Tuple[Response, mock_board_dto]:
    board_name = board_name or str(uuid.uuid4())
    password = password or str(uuid.uuid4())
    graduated_at = graduated_at or datetime.now() + timedelta(weeks=1)

    mock_request = {
        "board_name": board_name,
        "password": password,
        "bg_num": bg_num,
        "graduated_at": graduated_at.isoformat(),
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/board", json=mock_request)

    mock_dto = mock_board_dto(
        board_name=board_name,
        password=password,
        bg_num=bg_num,
        graduated_at=graduated_at,
    )

    return response, mock_dto
