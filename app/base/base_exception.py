from fastapi import HTTPException
from http import HTTPStatus

class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code, detail)
    
    def _responses(self) -> dict[int, str]:
        return {self.status_code: {
                "description": HTTPStatus(self.status_code).phrase,
                "content": {
                    "application/json":{
                        "example": {
                            "detail": self.detail
                        }
                    }
                }
            }
        }