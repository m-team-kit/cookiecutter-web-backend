"""Database configuration, methods, baseModels and dependencies."""
import logging
import re
from typing import Generator

from fastapi import FastAPI, Request
from sqlalchemy import engine, orm

from app.config import Settings

logger = logging.getLogger(__name__)


def init_app(app: FastAPI) -> None:
    """Initialize database configuration."""
    # pylint: disable=invalid-name
    settings: Settings = app.state.settings
    # Disconnect Handling - Pessimistic
    sql_engine = engine.create_engine(f"{settings.postgres_uri}", pool_pre_ping=True)
    app.state.sql_engine = sql_engine


camel2snake_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    return camel2snake_pattern.sub("_", name).lower()


class Base(orm.DeclarativeBase):
    """Base class for all models."""

    __name__: str

    # Generate __tablename__ automatically
    @orm.declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


def sessionmaker(sql_engine: engine.Engine) -> orm.sessionmaker:
    """Create a sessionmaker with manual flush and commit."""
    return orm.Session(bind=sql_engine, autoflush=False, autocommit=False)


async def get_session(request: Request) -> Generator:
    """Asynchronous generator to create a database session."""
    try:
        logger.debug("Creating database session.")
        database_session = sessionmaker(request.app.state.sql_engine)
        logger.debug("Yielding %s.", database_session)
        yield database_session
    finally:
        logger.debug("Closing database session.")
        database_session.close()
