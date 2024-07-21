from typing import Any

import structlog
from jwt import PyJWTError
from sqlalchemy.exc import IntegrityError

from src.core.enums.jwt_token import TokenTypeEnum
from src.core.exceptions.auth_exceptions import InvalidJWTException
from src.db_managers import UserManager
from src.models import User
from src.services.base import BaseService
from src.utils.security.jwt_token import JWTTokenBuilder

LOG = structlog.stdlib.get_logger()


class SecurityService(BaseService):
    """
    Service class for handling security-related operations, including token validation
    and user retrieval based on a provided JWT token.

    Attributes:
        user_manager (UserManager): Manager for user-related database operations.
        jwt_token_builder (JWTTokenBuilder): Utility for creating and decoding JWT tokens.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_manager = UserManager(self.session)
        self.jwt_token_builder = JWTTokenBuilder()

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

    def get_token_payload(self, token: str, token_type: str) -> dict[str, Any]:
        """
        Retrieves and verifies the token payload from the provided JWT token.

        Args:
            token (str): The JWT token to decode.
            token_type (str): The expected type of the token.

        Returns:
            dict[str, Any]: The payload of the JWT token.

        Raises:
            InvalidJWTException: If the token is invalid or verification fails.
        """
        try:
            token_payload = self.jwt_token_builder.decode_token(token)
            self.validate_token_type(token_type=token_type, token_payload=token_payload)
            return token_payload
        except PyJWTError as ex:
            LOG.error(f"Invalid token error. {ex}")
            raise InvalidJWTException()

    async def get_user_by_token_sub(self, sub: str) -> User:
        """
        Asynchronously retrieves a user by email (sub) from the token payload.

        Args:
            sub (str): The email (sub) from the token for retrieving the user.

        Returns:
            User: The user object corresponding to the provided email.

        Raises:
            InvalidJWTException: If retrieval fails due to integrity errors or user not found.
        """
        try:
            return await self.user_manager.get_by(filters={"email": sub})
        except IntegrityError as ex:
            LOG.error(f"Failed to retrieve user from token. {ex}")
            raise InvalidJWTException(detail="Invalid token. User not found")

    async def get_auth_user_by_access_token(self, access_token: str) -> User:
        """
        Asynchronously retrieves and validates the authenticated user based on the access token.

        Args:
            access_token (str): The access token used to retrieve the authenticated user.

        Returns:
            User: The authenticated user object.
        """
        return await self.get_user_by_token_sub(
            sub=self.get_token_payload(token=access_token, token_type=TokenTypeEnum.ACCESS.value).get("sub")
        )

    async def update_tokens(self, refresh_token: str) -> dict[str, str]:
        """
        Updates and generates new tokens based on the provided refresh token.

        Args:
            refresh_token (str): The refresh token used to generate new tokens.

        Returns:
            dict[str, str]: A dictionary containing the new access and refresh tokens.
        """
        user = await self.get_user_by_token_sub(
            sub=self.get_token_payload(token=refresh_token, token_type=TokenTypeEnum.REFRESH.value).get("sub")
        )
        return self.jwt_token_builder.get_tokens(user)
