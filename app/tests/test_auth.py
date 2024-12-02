from fastapi import status

from app.tests.mock.mock_board import mock_create_board
from app.tests.mock.mock_auth import mock_login


async def test_login_success() -> None:
    # Given
    response, mock_board_dto = await mock_create_board()

    # When
    login_response = await mock_login(board_name=mock_board_dto.board_name, password=mock_board_dto.password)
        
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert login_response.status_code == status.HTTP_200_OK
    assert "access_token" in login_response.json()["data"]


async def test_login_fail_password() -> None:
    # Given
    response, mock_board_dto = await mock_create_board()

    # When
    # 비밀번호는 uuid로 생성하므로 겹칠 수 없는 값으로 지정함
    login_response = await mock_login(board_name=mock_board_dto.board_name, password="11111111")
        
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_login_fail_board_name() -> None:
    # Given
    response, mock_board_dto = await mock_create_board()

    # When
    # 비밀번호는 uuid로 생성하므로 겹칠 수 없는 값으로 지정함
    login_response = await mock_login(board_name="11111111", password=mock_board_dto.password)
        
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED