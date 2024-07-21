from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.deps import get_security_service, get_user_service
from src.core.schemas import UserRead, UserRegister
from src.core.schemas.token.base import TokenInfo
from src.services import SecurityService, UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserRead)
async def register(user: UserRegister, service: UserService = Depends(get_user_service)):
    return await service.register_user(user)


@router.post("/login", response_model=TokenInfo)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_user_service)):
    return await service.login_user(form_data.username, form_data.password)


@router.post("/update-tokens", response_model=TokenInfo)
async def update_tokens(refresh_token: str, service: SecurityService = Depends(get_security_service)):
    return await service.update_tokens(refresh_token)
