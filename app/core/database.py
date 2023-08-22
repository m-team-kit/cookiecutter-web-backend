import re
from typing import Any

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from app.config import Settings


def init_app(app: FastAPI) -> None:
    """Initialize database configuration."""  # Disconnect Handling - Pessimistic
    settings: Settings = app.state.settings
    engine = create_engine(f"{settings.postgres_uri}", pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.state.SessionLocal = SessionLocal


camel2snake_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    return camel2snake_pattern.sub("_", name).lower()


class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


class Token(DeclarativeBase):
    subject: str
    issuer: str
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
