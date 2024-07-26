from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import Resource, build

from src.core.deps import get_google_oauth_flow, get_user_service
from src.services import UserService

router = APIRouter(prefix="/oauth/google", tags=["Google OAuth"])


@router.get("/login")
async def login(flow: Flow = Depends(get_google_oauth_flow)) -> RedirectResponse:
    return RedirectResponse(flow.authorization_url(access_type="offline", prompt="select_account")[0])


@router.get("/auth")
async def auth(
    request: Request,
    flow: Flow = Depends(get_google_oauth_flow),
    service: UserService = Depends(get_user_service),
):
    flow.fetch_token(authorization_response=str(request.url))
    user_info_service: Resource = build(serviceName="oauth2", version="v2", credentials=flow.credentials)
    user_info: dict[str, Any] = user_info_service.userinfo().get().execute()
    return await service.create_user_with_oauth(user_info=user_info)
