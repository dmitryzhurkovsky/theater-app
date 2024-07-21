from uuid import UUID

from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    user_id: UUID
    email: EmailStr
