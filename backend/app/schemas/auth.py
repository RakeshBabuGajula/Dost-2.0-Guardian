from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: str


class UserInfo(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str  # WORKER, SUPERVISOR, CONTROL_ROOM, ADMIN, AUDITOR
