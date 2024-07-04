from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.core.config.settings import settings
from src.core.deps import get_user_service
from src.services import UserService

router = APIRouter(prefix="/oauth/google", tags=["Google OAuth"])

GOOGLE_CLIENT_SECRETS = settings.AUTH_SETTINGS.GOOGLE_CLIENT_SECRETS_PATH
SCOPES = (
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
)


@router.get("/login")
async def login(request: Request) -> RedirectResponse:
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS,
        scopes=SCOPES,
        redirect_uri=request.url_for("auth"),
    )

    authorization_url, _ = flow.authorization_url(access_type="offline", prompt="select_account")
    return RedirectResponse(authorization_url)


@router.get("/auth")
async def auth(request: Request, service: UserService = Depends(get_user_service)):
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS,
        scopes=SCOPES,
        redirect_uri=request.url_for("auth"),
    )
    # Exchange the authorization code for an access token
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    # Get user info of the authenticated user
    credentials = flow.credentials
    user_info_service = build("oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    return await service.create_user_with_oauth(user_info=user_info)
