from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    JS analogy: `Depends(get_current_user)` is like `req.user` in Express after
    an auth middleware has run — except FastAPI injects it as a typed parameter.
    """
    return current_user
