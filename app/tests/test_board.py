from fastapi import status

from app.tests.mock.mock_board import mock_create_board


async def test_post_board_success() -> None:
    # Given

    # When
    response, mock_board_dto = await mock_create_board()

    # Then
    assert response.status_code == status.HTTP_200_OK


async def test_post_board_duplicate_name() -> None:
    # Given
    _, mock_board_dto_1 = await mock_create_board()

    # When
    response, mock_board_dto_2 = await mock_create_board(
        board_name=mock_board_dto_1.board_name
    )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_post_board_space_password() -> None:
    # Given
    password = "space yes"

    # When
    response, mock_board_dto = await mock_create_board(password=password)

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT
