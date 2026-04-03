from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import SessionLocal
from app.auth.service import decode_access_token

security = HTTPBearer()


def get_db():
    """
    Yield a database session, then close it when the request is done.

    JS analogy: this is like Express middleware that opens a DB connection
    at the start of a request and closes it in a finally block. The `yield`
    keyword is what makes this a generator — FastAPI calls it, gets the session,
    injects it into your route, then resumes after yield to run the cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Extract and validate the JWT from the Authorization header.
    Returns the User object if valid, raises 401 if not.

    JS analogy: this is your auth middleware, but instead of calling next(),
    FastAPI injects the return value directly into your route function.
    """
    # Import here (not at module level) to avoid a circular import:
    # dependencies.py -> users/models.py -> database.py -> (back to dependencies)
    from app.users.models import User

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
