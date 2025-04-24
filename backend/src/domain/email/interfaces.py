from typing import Any, Protocol


class EmailBuilderProtocol(Protocol):
    def build_reset_password_email(
        self, recipient: str, first_name: str, last_name: str, reset_password_link: str
    ) -> dict[str, Any]: ...


class EmailClientProtocol(Protocol):
    def send_email(self, data: dict[str, Any]) -> None: ...
