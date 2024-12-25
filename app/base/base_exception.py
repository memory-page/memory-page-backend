from fastapi import HTTPException
from typing import Any


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code, detail)

    def _responses(self) -> tuple[int, Any]:
        return (self.status_code, self.detail)
