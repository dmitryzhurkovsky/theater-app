from typing import Any

import structlog
from jwt import PyJWTError
from sqlalchemy.exc import IntegrityError

from src.core.exceptions.auth_exceptions import InvalidJWTException
from src.db_managers import UserManager
from src.models import User
from src.services.base import BaseService
from src.utils.security.jwt_token import jwt_token

LOG = structlog.stdlib.get_logger()


class SecurityService(BaseService):
    """
    Service class for handling security-related operations, including token validation
    and user retrieval based on a provided JWT token.

    Attributes:
        user_token (str): The JWT token of the user.
        user_manager (UserManager): Manager for user-related database operations.
    """

    def __init__(self, user_token: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_manager = UserManager(self.session)
        self.user_token = user_token

    @staticmethod
    def validate_token_type(token_type: str, token_payload: dict[str, Any]) -> bool:
        """
        Validates if the token type matches the expected type.

        Args:
            token_type (str): The expected type of the token.
            token_payload (dict[str, Any]): The payload of the token.

        Returns:
            bool: True if the token type is valid, raises InvalidJWTException otherwise.

        Raises:
            InvalidJWTException: If the token type does not match the expected type.
        """
        if token_type == token_payload.get("type"):
            return True

        LOG.error(f"Invalid token type {token_payload.get('type')} expected {token_type}")
        raise InvalidJWTException()

    def get_token_payload(self) -> dict[str, Any]:
        """
        Retrieves and verifies the token payload from the provided JWT token.

        Returns:
            dict[str, Any]: The payload of the JWT token.

        Raises:
            InvalidJWTException: If the token is invalid or verification fails.
        """
        try:
            return jwt_token.verify_token(self.user_token)
        except PyJWTError as ex:
            LOG.error(f"Invalid token error. {ex}")
            raise InvalidJWTException()

    async def get_user_by_token_sub(self, sub: str) -> User:
        """
        Asynchronously retrieves a user by email from the token payload.

        Args:
            sub (str): The sub of token for retrieving user.

        Returns:
            User: The user object corresponding to the provided email.

        Raises:
            InvalidJWTException: If retrieval fails due to integrity errors or user not found.
        """
        try:
            return await self.user_manager.get_by_email(filters={"email": sub})
        except IntegrityError as ex:
            LOG.error(f"Failed to retrieve user from token. {ex}")
            raise InvalidJWTException(detail="Invalid token. User not found")

    async def get_auth_user(self, token_type: str) -> User:
        """
        Asynchronously retrieves and validates the authenticated user based on the token type.

        Args:
            token_type (str): The expected type of the token.

        Returns:
            User: The authenticated user object.
        """
        token_payload = self.get_token_payload()
        self.validate_token_type(token_type, token_payload)

        return await self.get_user_by_token_sub(sub=token_payload.get("sub"))
