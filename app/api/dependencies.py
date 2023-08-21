from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import crud, models

bearer_token = HTTPBearer()
bearer_secret = HTTPBearer()


async def get_session(
        request: Request
) -> Generator:  # fmt: skip
    """Yield database session generator."""
    try:
        database_session = request.app.state.SessionLocal()
        yield database_session
    finally:
        database_session.close()


async def get_user(
    request: Request,
    session: Session = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> models.User:
    token_info = request.app.state.flaat.get_user_infos_from_access_token(token.credentials)
    return crud.user.get(session, subject=token_info.subject, issuer=token_info.issuer)


async def check_secret(
    request: Request,
    secret: HTTPAuthorizationCredentials = Depends(bearer_secret),
) -> None:
    correct = request.app.state.settings.secret == secret.credentials
    if not correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect secret",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return None
