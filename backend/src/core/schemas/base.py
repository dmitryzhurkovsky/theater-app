from typing import Any

from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    data: Any

    class Config:
        from_attributes = True


class MessageResponseSchema(BaseModel):
    message: str
