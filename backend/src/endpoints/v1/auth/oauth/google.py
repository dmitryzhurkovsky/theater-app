from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from googleapiclient.discovery import Resource, build

from src.core.deps import GoogleOAuthFlow, UserServiceDep

router = APIRouter(prefix="/oauth/google", tags=["Google OAuth"])


@router.get("/login")
async def login(flow: GoogleOAuthFlow) -> RedirectResponse:
    return RedirectResponse(flow.authorization_url(access_type="offline", prompt="select_account")[0])


@router.get("/auth")
async def auth(
    request: Request,
    flow: GoogleOAuthFlow,
    service: UserServiceDep,
):
    flow.fetch_token(authorization_response=str(request.url))
    user_info_service: Resource = build(serviceName="oauth2", version="v2", credentials=flow.credentials)
    user_info: dict[str, Any] = user_info_service.userinfo().get().execute()
    return await service.create_user_with_oauth(user_info=user_info)
