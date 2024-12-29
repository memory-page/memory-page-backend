from fastapi import status

from app.base.base_exception import BaseHTTPException


class TooShortNameException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이름이 너무 짧습니다."
        )


class TooLongNameException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이름이 너무 깁니다."
        )


class DuplicateNameException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="중복된 이름이 존재합니다."
        )


class CanNotUseSpaceFrontEndBackInNameException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이름의 앞과 뒤는 공백일 수 없습니다.",
        )


class OnlyKrEngNumSpecialInNameException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이름은 한글, 영어, 숫자, 특수문자만 사용할 수 있습니다.",
        )


class CanNotUseBadWordInNameException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이름에 비속어는 사용할 수 없습니다.",
        )


class CanNotUseSpaceInPasswordException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호에는 띄어쓰기를 사용할 수 없습니다.",
        )


class MinLengthInPasswordException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호는 최소 4자 이상이어야 합니다.",
        )


class WrongNameOrPasswordInValidateLoginException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이름 또는 비밀번호가 올바르지 않습니다.",
        )


class ValidateDateStrException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="날짜 문자열의 형식이 올바르지 않습니다.",
        )


class DoesNotExistBoardException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 칠판입니다."
        )


class CanNotUseBadWordInContentException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="내용에 비속어는 사용할 수 없습니다.",
        )


class ContentLengthException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="내용은 1자 이상 100자 이하로 작성해야 합니다.",
        )


class ValidateAuthorLengthException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이름은 1자 이상 10자 이하로 작성해야 합니다.",
        )


class DoesNotExistMemoException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않은 메모입니다."
        )


class NotEqualMemoIdAndBoardIdException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="메모가 요청한 board_id에 속하지 않습니다.",
        )


class ExpiredTokenException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 만료되었습니다."
        )


class InvalidTokenException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다."
        )


class InvalidTokenDataException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰 데이터가 유효하지 않습니다.",
        )


class BoardGraduatedException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="새해부터 조회가 가능합니다.",
        )


class SameLocateIdxMemoException(BaseHTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="메모 위치가 중복되었습니다.",
        )
