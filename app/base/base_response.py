from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    detail: str
    data: BaseModel
