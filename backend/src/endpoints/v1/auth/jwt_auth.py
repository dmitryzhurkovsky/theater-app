from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from src.core.deps import EmailServiceDep, SecurityServiceDep, UserServiceDep
from src.core.schemas import (
    MessageResponseSchema,
    TokenInfo,
    UserForgotPassword,
    UserRead,
    UserRegister,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/forgot-password", response_model=MessageResponseSchema)
async def forgot_password(
    user_info: UserForgotPassword,
    background_tasks: BackgroundTasks,
    service: UserServiceDep,
    email_service: EmailServiceDep,
):
    reset_password_email_data = await service.get_reset_password_email_data(email=user_info.email)

    if reset_password_email_data:
        background_tasks.add_task(email_service.send_reset_password_email, **reset_password_email_data.model_dump())

    return {"message": f"Message was successfully sent to {user_info.email}"}


@router.post("/reset-password", response_model=MessageResponseSchema)
async def reset_password(token: Annotated[str, Form()], new_password: Annotated[str, Form()], service: UserServiceDep):
    await service.reset_password(token=token, new_password=new_password)
    return {"message": "Your password has been reset successfully."}


@router.post("/signup", response_model=UserRead)
async def register(user: UserRegister, service: UserServiceDep):
    return await service.register_user(user)


@router.post("/login", response_model=TokenInfo)
async def login(service: UserServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    return await service.login_user(form_data.username, form_data.password)


@router.post("/update-tokens", response_model=TokenInfo)
async def update_tokens(refresh_token: str, service: SecurityServiceDep):
    return await service.update_tokens(refresh_token)
