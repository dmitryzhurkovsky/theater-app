from src.domain.email import EmailBuilderProtocol, EmailClientProtocol


class EmailService:
    def __init__(self, email_builder: EmailBuilderProtocol, email_client: EmailClientProtocol):
        self.email_builder = email_builder
        self.email_client = email_client

    def send_reset_password_email(
        self, user_email: str, first_name: str, last_name: str, reset_password_link: str
    ) -> None:
        reset_password_email = self.email_builder.build_reset_password_email(
            recipient=user_email, first_name=first_name, last_name=last_name, reset_password_link=reset_password_link
        )

        self.email_client.send_email(data=reset_password_email)
