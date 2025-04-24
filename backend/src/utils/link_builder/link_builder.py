from src.core.config.settings import settings


def build_reset_password_link(token: str) -> str:
    return f"{settings.MOBILE_APP_BASE_URL}/reset-password?token={token}"
