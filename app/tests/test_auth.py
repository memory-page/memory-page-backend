from fastapi import status

from app.tests.mock.mock_board import mock_create_board
from app.tests.mock.mock_auth import mock_login


async def test_login_success() -> None:
    # Given
    _, mock_board_dto = await mock_create_board()

    # When
    login_response = await mock_login(board_name=mock_board_dto.board_name, password=mock_board_dto.password)
        
    # Then
    assert login_response.status_code == status.HTTP_200_OK
    assert "access_token" in login_response.json()["data"]
