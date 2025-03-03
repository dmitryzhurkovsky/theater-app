from typing import Generic, TypeVar

from pydantic import BaseModel

GenericBaseModelType = TypeVar("GenericBaseModel", bound=BaseModel)


class GenericBaseModel(Generic[GenericBaseModelType]):
    pass


class PaginationConfig(BaseModel):
    default_per_page: int = 100
    max_per_page: int = 200


class ControllerConfig(BaseModel):
    pagination: PaginationConfig = PaginationConfig()
