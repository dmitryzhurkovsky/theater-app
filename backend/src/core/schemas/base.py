from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: Any


class MessageResponseSchema(BaseModel):
    message: str
