from functools import cached_property
from typing import Any

from src.core.config.settings import settings
from src.domain import EmailBuilderProtocol


class MailjetEmailBuilder(EmailBuilderProtocol):
    reset_password_template_id: int = settings.MAILJET.MJ_RESET_PASSWORD_TEMPLATE_ID
    sender_email: str = settings.MAILJET.MJ_SENDER_EMAIL

    @cached_property
    def globals_section(self) -> dict[str, Any]:
        return {
            "From": {
                "Email": settings.MAILJET.MJ_SENDER_EMAIL,
                "Name": "theater-app",
            },
            "TemplateLanguage": True,
        }

    def build_base_email(self) -> dict[str, Any]:
        return {"Globals": self.globals_section, "Messages": []}

    def build_reset_password_email(
        self, recipient: str, first_name: str, last_name: str, reset_password_link: str
    ) -> dict[str, Any]:
        reset_password_email = self.build_base_email()
        reset_password_email["Messages"].append(
            {
                "To": [{"Email": recipient}],
                "TemplateID": self.reset_password_template_id,
                "Variables": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "reset_password_link": reset_password_link,
                },
            }
        )

        return reset_password_email
