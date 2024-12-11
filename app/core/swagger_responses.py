from typing import Dict, Any

from app.core.exception import (
    CanNotUseBadWordInContentException,
    CanNotUseBadWordInNameException,
    CanNotUseSpaceFrontEndBackInNameException,
    CanNotUseSpaceInPasswordException,
    ContentLengthException,
    DoesNotExistBoardException,
    DoesNotExistMemoException,
    DuplicateNameException,
    ExpiredTokenException,
    InvalidTokenDataException,
    MinLengthInPasswordException,
    NotEqualMemoIdAndBoardIdException,
    OnlyKrEngNumSpecialInNameException,
    TooLongNameException,
    TooShortNameException,
    ValidateAuthorLengthException,
    ValidateDateStrException,
    WrongNameOrPasswordInValidateLoginException,
)
from app.utils.responses_creater import ResponsesCreater

"""TODO: 구조 더 이쁘게 수정해야 됨
API 내부에 발생되는 모든 Exception을 명시해주어야 함
더 좋은 방법이 있을텐데 일단 내머리(2024-12-08 11:22 이인규)로는 이정도로..
"""

response_creater = ResponsesCreater()


def post_board_responses() -> Dict[Any, Any]:
    return response_creater.responses_creater(
        [
            DuplicateNameException()._responses(),
            TooShortNameException()._responses(),
            TooLongNameException()._responses(),
            CanNotUseSpaceFrontEndBackInNameException()._responses(),
            OnlyKrEngNumSpecialInNameException()._responses(),
            CanNotUseBadWordInNameException()._responses(),
            CanNotUseSpaceInPasswordException()._responses(),
            CanNotUseSpaceInPasswordException()._responses(),
            MinLengthInPasswordException()._responses(),
            ValidateDateStrException()._responses(),
        ]
    )


def post_board_login_responses() -> Dict[Any, Any]:
    return response_creater.responses_creater(
        [
            CanNotUseSpaceInPasswordException()._responses(),
            CanNotUseSpaceInPasswordException()._responses(),
            MinLengthInPasswordException()._responses(),
            WrongNameOrPasswordInValidateLoginException()._responses(),
            WrongNameOrPasswordInValidateLoginException()._responses(),
        ]
    )


def post_board_validate_responses() -> Dict[Any, Any]:
    return response_creater.responses_creater(
        [
            DuplicateNameException()._responses(),
            TooShortNameException()._responses(),
            TooLongNameException()._responses(),
            CanNotUseSpaceFrontEndBackInNameException()._responses(),
            OnlyKrEngNumSpecialInNameException()._responses(),
            CanNotUseBadWordInNameException()._responses(),
            CanNotUseSpaceInPasswordException()._responses(),
            CanNotUseSpaceInPasswordException()._responses(),
            MinLengthInPasswordException()._responses(),
        ]
    )


def post_board_boardid_memo_responses() -> Dict[Any, Any]:
    return response_creater.responses_creater(
        [
            DoesNotExistBoardException()._responses(),
            DoesNotExistBoardException()._responses(),
            CanNotUseBadWordInNameException()._responses(),
            CanNotUseSpaceFrontEndBackInNameException()._responses(),
            ValidateAuthorLengthException()._responses(),
            CanNotUseBadWordInContentException()._responses(),
            ContentLengthException()._responses(),
        ]
    )


def get_memo_momoid_responses() -> Dict[Any, Any]:
    return response_creater.responses_creater(
        [
            DoesNotExistMemoException()._responses(),
            DoesNotExistMemoException()._responses(),
            NotEqualMemoIdAndBoardIdException()._responses(),
        ]
    )


def get_board_boardid_responses() -> Dict[Any, Any]:
    return response_creater.responses_creater(
        [
            DoesNotExistBoardException()._responses(),
            ExpiredTokenException()._responses(),
            InvalidTokenDataException()._responses(),
        ]
    )
