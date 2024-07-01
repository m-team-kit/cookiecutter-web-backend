"""Exception handlers for the API."""

# pylint: disable=unused-argument,missing-module-docstring
import logging

from fastapi import FastAPI, HTTPException, Request, status
from flaat.exceptions import FlaatForbidden, FlaatUnauthenticated
from sqlalchemy.orm.exc import NoResultFound
from cookiecutter.exceptions import CookiecutterException

logger = logging.getLogger(__name__)


async def unauthorized(request: Request, exc: FlaatUnauthenticated):
    """Handle unauthorized exceptions."""
    logger.debug("Authentication error: %s", exc)
    info = {"type": "authentication", "loc": ["header", "bearer"], "msg": exc.args[0]}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
        detail=[info],
    )


async def forbidden(request: Request, exc: FlaatForbidden):
    """Handle forbidden exceptions."""
    logger.debug("Authentication error: %s", exc)
    info = {"type": "authentication", "loc": ["header", "bearer"], "msg": exc.args[0]}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        headers={"WWW-Authenticate": "Bearer"},
        detail=[info],
    )


async def not_found(request: Request, exc: NoResultFound):
    """Handle not found exceptions."""
    logger.debug("Template %s not found: %s", request.path_params, exc)
    info = {"type": "not_found", "loc": ["path", "uuid"], "msg": exc.args[0]}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=[info],
    )


async def server_error(request: Request, exc: Exception):
    """Handle server error exceptions (default exceptions)."""
    if isinstance(exc, HTTPException):  # Catch only not defined exceptions
        raise exc
    if isinstance(exc, CookiecutterException):  # Catch only CookiecutterExceptions
        logger.error("Cookiecutter error: %s", exc)
        info = {"type": "cookiecutter_error", "loc": ["cookiecutter.json"], "msg": exc.args[0]}
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[info],
        )
    logger.error("Server error: %s", exc)
    info = {"type": "server_error", "loc": ["server"], "msg": "Internal Server Error"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=[info],
    )


async def not_implemented(request: Request, exc: NotImplementedError):
    """Handle not implemented exceptions."""
    logger.debug("Not implemented error: %s", exc)
    info = {"type": "not_implemented", "loc": ["gitLink", "gitCheckout", "cookiecutter.json"], "msg": exc.args[0]}
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=[info],
    )


def add_exception_handlers(api: FastAPI):
    """Add exception handlers to the API."""
    api.add_exception_handler(FlaatUnauthenticated, unauthorized)
    api.add_exception_handler(FlaatForbidden, forbidden)
    api.add_exception_handler(NoResultFound, not_found)
    api.add_exception_handler(Exception, server_error)
    api.add_exception_handler(NotImplementedError, not_implemented)
