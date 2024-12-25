from httpx import AsyncClient, ASGITransport, Response
from datetime import datetime, timedelta
from unittest.mock import patch
from typing import Tuple
import dataclasses
import uuid

from app.main import app


@dataclasses.dataclass(kw_only=True, frozen=True)
class mock_board_dto:
    board_name: str
    password: str
    bg_num: int
    graduated_at: str


async def mock_create_board(
    board_name: str | None = None,
    password: str | None = None,
    bg_num: int = 0,
    graduated_at: str | None = None,
) -> Tuple[Response, mock_board_dto]:
    """
    칠판 생성 모킹 함수

    Parameter
    ---
    board_name: str | None = None, 칠판 이름
    password: str | None = None, 비밀번호
    bg_num: int = 0, 배경 번호
    graduated_at: datetime | None = None, 졸업 날짜

    Return
    ---
    Response: Response, request 결과
    mock_board_dto: mock_board_dto, 생성된 칠판 정보
    """
    is_mock_board_name = board_name is None
    board_name = board_name or str(uuid.uuid4())
    password = password or str(uuid.uuid4())
    graduated_at = (
        graduated_at or str(datetime.now() + timedelta(weeks=1)).split(" ")[0]
    )

    mock_request = {
        "board_name": board_name,
        "password": password,
        "bg_num": bg_num,
        "graduated_at": graduated_at,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        if is_mock_board_name:
            with patch("app.domain.board.service.BoardService._length_checker"):
                response = await client.post("/board", json=mock_request)
        else:
            response = await client.post("/board", json=mock_request)

    mock_dto = mock_board_dto(
        board_name=board_name,
        password=password,
        bg_num=bg_num,
        graduated_at=graduated_at,
    )

    return response, mock_dto
