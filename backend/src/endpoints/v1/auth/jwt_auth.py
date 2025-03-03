from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.deps import SecurityServiceDep, UserServiceDep
from src.core.schemas import UserRead, UserRegister
from src.core.schemas.token.base import TokenInfo

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserRead)
async def register(user: UserRegister, service: UserServiceDep):
    return await service.register_user(user)


@router.post("/login", response_model=TokenInfo)
async def login(service: UserServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    return await service.login_user(form_data.username, form_data.password)


@router.post("/update-tokens", response_model=TokenInfo)
async def update_tokens(refresh_token: str, service: SecurityServiceDep):
    return await service.update_tokens(refresh_token)
