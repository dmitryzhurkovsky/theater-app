from typing import Any

import structlog
from mailjet_rest import Client

from src.core.config.settings import settings
from src.domain import EmailClientProtocol

LOG = structlog.stdlib.get_logger()


class MailjetEmailClient(EmailClientProtocol):
    def __init__(self) -> None:
        self.api_key = settings.MAILJET.MJ_API_KEY_PUBLIC
        self.api_secret = settings.MAILJET.MJ_API_KEY_PRIVATE
        self.version = settings.MAILJET.MJ_CLIENT_VERSION
        self.client = Client(auth=(self.api_key, self.api_secret), version=self.version)

    def send_email(self, data: dict[str, Any]) -> None:
        result = self.client.send.create(data=data)
        LOG.info(f"Mailjet send email result: {result.status_code}")
