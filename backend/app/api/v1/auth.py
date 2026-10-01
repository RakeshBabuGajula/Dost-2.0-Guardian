from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse, UserInfo
from app.security.auth import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication & Boundary"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Development authentication boundary.
    Validates synthetic development roles and issues JWT tokens.
    """
    if request.username == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Determine role based on username or default to WORKER / CONTROL_ROOM
    role = "CONTROL_ROOM"
    if "worker" in request.username.lower():
        role = "WORKER"
    elif "supervisor" in request.username.lower():
        role = "SUPERVISOR"
    elif "admin" in request.username.lower():
        role = "ADMIN"
    elif "auditor" in request.username.lower():
        role = "AUDITOR"

    token = create_access_token(
        user_id=f"usr-{request.username}",
        username=request.username,
        role=role,
    )

    return TokenResponse(
        access_token=token,
        user_id=f"usr-{request.username}",
        username=request.username,
        role=role,
    )


@router.get("/me", response_model=UserInfo)
def get_me(current_user: UserInfo = Depends(get_current_user)):
    """Returns currently authenticated user profile & permissions boundary role."""
    return current_user
