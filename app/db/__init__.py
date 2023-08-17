from typing import Generator

from app.db.session import SessionLocal


async def get_session() -> Generator:
    """Yield database session generator."""
    try:
        database_session = SessionLocal()
        yield database_session
    finally:
        database_session.close()
