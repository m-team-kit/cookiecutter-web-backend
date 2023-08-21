from typing import Generator

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import crud, models

bearer_token = HTTPBearer()


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
