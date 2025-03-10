from typing import Generic, Type, TypeVar

from pydantic import BaseModel

GenericBaseModel = TypeVar("GenericBaseModel", bound=BaseModel)
GenericBaseModelType = Type[GenericBaseModel]


class PaginationConfig(BaseModel):
    default_per_page: int = 100
    max_per_page: int = 200


class ControllerConfig(BaseModel):
    pagination: PaginationConfig = PaginationConfig()
