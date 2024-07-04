from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.deps import get_user_from_access_token, get_user_service
from src.core.schemas import UserRead, UserRegister
from src.core.schemas.token.base import TokenInfo
from src.services import SecurityService, UserService
from src.utils.security.jwt_token import jwt_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=UserRead,
    response_model_exclude_none=True,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to create user"},
                },
            },
        },
        409: {
            "description": "Registration Error",
            "content": {
                "application/json": {
                    "example": {"detail": "User already exists"},
                },
            },
        },
    },
)
async def register(user: UserRegister, service: UserService = Depends(get_user_service)):
    return await service.register_user(user)


@router.post(
    "/login",
    response_model=TokenInfo,
    responses={
        401: {
            "description": "Authentication Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"},
                },
            },
        },
    },
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
    token_data = await service.login_user(form_data.username, form_data.password)
    return TokenInfo(access_token=token_data.get("access_token"), refresh_token=token_data.get("refresh_token"))


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    responses={
        401: {
            "description": "Authentication Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"},
                },
            },
        },
    },
)
async def update_access_token(user: SecurityService = Depends(get_user_from_access_token)):
    return TokenInfo(access_token=jwt_token.create_access_token(user))
