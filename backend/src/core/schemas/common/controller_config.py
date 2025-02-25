from typing import TypeVar

from pydantic import BaseModel

GenericBaseModel = TypeVar("GenericBaseModel", bound=BaseModel)


class PaginationConfig(BaseModel):
    default_per_page: int = 100
    max_per_page: int = 200


class ControllerConfig(BaseModel):
    pagination: PaginationConfig = PaginationConfig()
