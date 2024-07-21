from datetime import datetime, timedelta
from functools import cached_property
from typing import Any

import jwt

from src.core.config.settings import settings
from src.core.enums.jwt_token import TokenTypeEnum
from src.models import User


class JWTTokenBuilder:
    """
    JWTTokenBuilder is a utility class for building JSON Web Tokens (JWT) for authentication and authorization purposes.

    Attributes:
        private_key (str): The private key used for signing the JWT tokens.
        public_key (str): The public key used for verifying the JWT tokens.
        algorithm (str): The algorithm used for encoding and decoding the JWT tokens.
        issuer (str): The issuer of the JWT tokens, typically identifying the application or service issuing the tokens.
        expire_minutes (timedelta): The expiration time for access tokens.
        expire_days (timedelta): The expiration time for refresh tokens.
    """

    private_key: str = settings.AUTH.PRIVATE_KEY_PATH
    public_key: str = settings.AUTH.PUBLIC_KEY_PATH
    algorithm: str = settings.AUTH.ALGORITHM
    issuer: str = settings.AUTH.TOKEN_ISSUER
    expire_minutes: timedelta = settings.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES
    expire_days: timedelta = settings.AUTH.REFRESH_TOKEN_EXPIRE_DAYS

    @cached_property
    def set_jwt_token_header(self) -> dict[str, str]:
        """
        Returns the JWT token header.

        Returns:
            dict[str, str]: The JWT token header with type and algorithm.
        """
        return {"typ": "JWT", "alg": self.algorithm}

    def update_payload(self, payload: dict[str, Any], expire: timedelta) -> dict[str, Any]:
        """
        Updates the given payload with expiration (`exp`), not-before (`nbf`),
        and issued-at (`iat`) times, and adds the issuer (`iss`).

        Args:
            payload (dict): The original payload.
            expire (timedelta): The expiration time to be added to the payload.

        Returns:
            dict: The updated payload with `exp`, `nbf`, `iat`, and `iss` fields.
        """
        datetime_now: datetime = datetime.now()

        payload_copy = payload.copy()
        payload_copy.update(
            {
                "iss": self.issuer,
                "exp": datetime_now + expire,
                "nbf": datetime_now,
                "iat": datetime_now,
            }
        )
        return payload_copy

    def create_jwt_token(self, payload: dict[str, Any], expire: timedelta) -> str:
        """
        Creates a JWT token with the given payload and expiration time.

        Args:
            payload (dict[str, Any]): The payload to be encoded into the JWT token.
            expire (timedelta): The expiration time for the token.

        Returns:
            str: The encoded JWT token.
        """
        return jwt.encode(
            headers=self.set_jwt_token_header,
            payload=self.update_payload(payload=payload, expire=expire),
            key=self.private_key,
            algorithm=self.algorithm,
        )

    def create_access_token(self, user: User) -> str:
        """
        Creates an access token for the given user.

        Args:
            user (User): The user for whom the access token is being created.

        Returns:
            str: The encoded access token.
        """
        return self.create_jwt_token(
            payload={
                "type": TokenTypeEnum.ACCESS.value,
                "sub": user.email,
                "user_id": str(user.id),
            },
            expire=self.expire_minutes,
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        """
        Verifies the given access token and returns the decoded payload.

        Args:
            token (str): The access token to be verified.

        Returns:
            dict[str, Any]: The decoded payload of the token.
        """
        return jwt.decode(jwt=token, key=self.public_key, algorithms=[self.algorithm])

    def create_refresh_token(self, user: User) -> str:
        """
        Creates a refresh token for the given user.

        Args:
            user (User): The user for whom the refresh token is being created.

        Returns:
            str: The encoded refresh token.
        """
        return self.create_jwt_token(
            payload={"type": TokenTypeEnum.REFRESH.value, "sub": user.email},
            expire=self.expire_days,
        )

    def get_tokens(self, user: User) -> dict[str, str]:
        """
        Generates a pair of access and refresh tokens for the given user.

        Args:
            user (User): The user for whom the tokens are being generated.

        Returns:
            dict[str, str]: A dictionary containing the access and refresh tokens.
        """
        return {"access_token": self.create_access_token(user), "refresh_token": self.create_refresh_token(user)}
