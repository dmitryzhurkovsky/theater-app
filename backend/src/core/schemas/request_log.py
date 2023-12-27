from typing import Self

from pydantic import BaseModel, Field, model_validator
from src.utils import normalise_dict, prettify


class RequestLogUser(BaseModel):
    id: int | None


class RequestLogClientSchema(BaseModel):
    ip: str | int | None
    port: str | int | None


class RequestLogHttpSchema(BaseModel):
    url: str | None
    status_code: int | None
    method: str | None
    version: str | None


class RequestLogSchema(BaseModel):
    request_id: str | None
    client: RequestLogClientSchema | None
    http: RequestLogHttpSchema | None
    user: RequestLogUser | None
    duration: int | None
    headers: dict | None
    query_params: dict | None
    path_params: dict | None
    body_json: dict | None
    body_json_normalised: dict | None = None

    @model_validator(mode="after")
    def set_body_normalised(self) -> Self:
        if self.body_json is not None:
            self.body_json_normalised = normalise_dict(self.body_json)

        return self

    def get_entry(self, normalise_body: bool = True) -> dict:
        exclude = {"body_json_normalised"} if not normalise_body else {}
        return prettify(self.model_dump(exclude_none=True, exclude=exclude))
