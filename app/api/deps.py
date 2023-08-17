from typing import Generator

from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core import security
from app.db.session import SessionLocal

bearer_token = HTTPBearer()


async def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user(
    db: Session = Depends(get_db),
    token: str = Depends(bearer_token),
) -> str:  # models.User:
    token_info = security.flaat.get_user_infos_from_access_token(token.credentials)
    subiss = (token_info.subject, token_info.issuer)
    # db_user = crud.user.get(db=db, id=subiss)
    return subiss
