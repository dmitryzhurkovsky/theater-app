from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponseSchema(BaseModel):
    message: str
