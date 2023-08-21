from typing import Any

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from app.config import Settings


def init_app(app: FastAPI, settings: Settings) -> None:
    """Initialize database configuration."""  # Disconnect Handling - Pessimistic
    engine = create_engine(f"{settings.postgres_uri}", pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.state.SessionLocal = SessionLocal


class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Token(DeclarativeBase):
    subject: str
    issuer: str
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
