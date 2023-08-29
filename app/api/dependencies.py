import logging
import tempfile
from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from flaat.exceptions import FlaatUnauthenticated
from sqlalchemy.orm import Session

from app import models, schemas

logger = logging.getLogger(__name__)
bearer_token = HTTPBearer(auto_error=False)
bearer_secret = HTTPBearer(auto_error=False)


async def get_session(
        request: Request
) -> Generator:  # fmt: skip
    """Yield database session generator."""

    try:
        logger.debug("Creating database session.")
        database_session = request.app.state.SessionLocal()
        yield database_session

    finally:
        logger.debug("Closing database session.")
        database_session.close()


async def temp_folder() -> Generator:
    """Yield temporary folder generator."""

    logger.debug("Creating temporary folder.")
    with tempfile.TemporaryDirectory() as tempdir:
        yield tempdir
        logger.debug("Removing temporary folder.")


async def get_user(
    request: Request,
    session: Session = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> models.User:
    """Returns user from token."""

    try:
        logger.debug("If no token present raise Unauthenticated.")
        if not token:
            raise FlaatUnauthenticated("Not authenticated")

        logger.debug("Getting user from token. %s", token.credentials)
        token_info = request.app.state.flaat.get_user_infos_from_access_token(token.credentials)

        logger.debug("Checking if token is valid.")
        if not token_info:
            raise FlaatUnauthenticated("Not authenticated")

    except FlaatUnauthenticated as err:
        logger.debug("Not authenticated.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    logger.debug("Getting user from database.")
    user = session.get(models.User, (token_info.subject, token_info.issuer))
    if not user:  # If user not in the database, register it
        logger.debug("Creating user in database.")
        user = models.User(subject=token_info.subject, issuer=token_info.issuer)
        session.add(user)
        session.commit()

    return user


async def check_secret(
    request: Request,
    secret: HTTPAuthorizationCredentials = Depends(bearer_secret),
) -> None:
    """Checks if secret is correct."""

    try:
        logger.debug("If no secret present raise ValueError.")
        if not secret:
            raise KeyError("Not authenticated")

        logger.debug("Checking secret.")
        correct = request.app.state.settings.secret == secret.credentials
        if not correct:
            logger.debug("Incorrect secret.")
            raise ValueError("Incorrect secret")

    except KeyError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.args[0],
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=err.args[0],
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    return None
