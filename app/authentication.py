"""Authentication module."""
import logging
from typing import Generator

from fastapi import Depends, FastAPI, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from flaat.exceptions import FlaatForbidden, FlaatUnauthenticated
from flaat.fastapi import Flaat
from sqlalchemy.orm import Session

from app import config, database, models
from app.config import Settings

logger = logging.getLogger(__name__)
bearer_token = HTTPBearer(auto_error=False)
bearer_secret = HTTPBearer(auto_error=False)


def init_app(app: FastAPI) -> None:
    """Initialize security configuration."""
    settings: Settings = app.state.settings
    app.state.flaat = Flaat()
    op_list = [str(x) for x in settings.trusted_op]
    app.state.flaat.set_trusted_OP_list(op_list)


async def get_user(
    request: Request,
    session: Session = Depends(database.get_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Generator:
    """Returns user from token."""

    logger.debug("If no token present raise Unauthenticated.")
    if not token:
        raise FlaatUnauthenticated("Not authenticated")

    logger.debug("Getting user from token. %s", token.credentials)
    token_info = request.app.state.flaat.get_user_infos_from_access_token(token.credentials)

    logger.debug("Checking if token is valid.")
    if not token_info:
        raise FlaatUnauthenticated("Not authenticated")

    logger.debug("Getting user from database.")
    user = session.get(models.User, (token_info.subject, token_info.issuer))
    if not user:  # If user not in the database, register it
        logger.debug("Creating user in database.")
        user = models.User(subject=token_info.subject, issuer=token_info.issuer)
        session.add(user)
        session.commit()

    yield user


async def check_secret(
    settings: Settings = Depends(config.get_settings),
    secret: HTTPAuthorizationCredentials = Depends(bearer_secret),
) -> None:
    """Checks if secret is correct."""

    logger.debug("If no secret present raise ValueError.")
    if not secret:
        raise FlaatUnauthenticated("Not authenticated")

    logger.debug("Checking secret.")
    if settings.admin_secret != secret.credentials:
        logger.debug("Incorrect secret.")
        raise FlaatForbidden("Incorrect secret")
