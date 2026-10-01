from datetime import datetime, timedelta, timezone
from typing import Optional, List, Callable
import jwt
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.schemas.auth import UserInfo

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def create_access_token(user_id: str, username: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=24)

    to_encode = {
        "sub": user_id,
        "username": username,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Depends(oauth2_scheme),
) -> UserInfo:
    auth_token = token
    if not auth_token and authorization:
        if authorization.startswith("Bearer "):
            auth_token = authorization.split(" ")[1]
        else:
            auth_token = authorization

    # Development auth fallback if no header passed
    if not auth_token:
        return UserInfo(
            id="usr-dev-control-room",
            username="control_room_operator",
            email="operator@dostguardian.railway",
            full_name="Control Room Operator (Dev)",
            role="CONTROL_ROOM",
        )

    try:
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims",
            )
        return UserInfo(
            id=user_id,
            username=username or "user",
            email=f"{username}@dostguardian.railway",
            full_name=username or "User",
            role=role,
        )
    except jwt.PyJWTError:
        # Development fallback for local synthetic tokens
        return UserInfo(
            id="usr-dev-worker",
            username="ramesh_kumar",
            email="ramesh@dostguardian.railway",
            full_name="Ramesh Kumar",
            role="WORKER",
        )

# Alias for get_current_user
get_current_active_user = get_current_user

def require_roles(allowed_roles: List[str]) -> Callable:
    """Dependency checker to enforce role-based access control (RBAC)."""
    def role_checker(user: UserInfo = Depends(get_current_user)) -> UserInfo:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{user.role}' is not authorized. Allowed roles: {allowed_roles}"
            )
        return user
    return role_checker
