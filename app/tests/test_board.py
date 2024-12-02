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
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_too_short() -> None:
    # Given
    mock_board_name = "닉"

    # When
    response, _ = await mock_create_board(board_name=mock_board_name)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_too_long_kor() -> None:
    # Given
    mock_board_name = "엄청나게긴닉네임이라서통과되지못해요"

    # When
    response, _ = await mock_create_board(board_name=mock_board_name)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_too_long_eng() -> None:
    # Given
    mock_board_name = "TooLongNickNameNoPass"

    # When
    response, _ = await mock_create_board(board_name=mock_board_name)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_no_front_space() -> None:
    # Given
    mock_board_name = " 앞공백이름"

    # When
    response, _ = await mock_create_board(board_name=mock_board_name)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_no_back_space() -> None:
    # Given
    mock_board_name = "뒤공백이름 "

    # When
    response, _ = await mock_create_board(board_name=mock_board_name)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_only_kor_eng_num_special() -> None:
    # Given
    mock_board_name = "이모지닉네임😀"

    # When
    response, _ = await mock_create_board(board_name=mock_board_name)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_can_not_use_bad_word() -> None:
    # Given
    mock_board_name = "테스트욕할거야 시 발"

    # When
    response, _ = await mock_create_board(board_name=mock_board_name)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_post_board_space_password() -> None:
    # Given
    password = "space yes"

    # When
    response, mock_board_dto = await mock_create_board(password=password)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
