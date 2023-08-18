from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from flaat.fastapi import Flaat
from sqlalchemy.orm import Session

from app import db
from app import crud
from app.core.config import settings
from app import models

bearer_token = HTTPBearer()
flaat = Flaat()
flaat.set_trusted_OP_list([str(x) for x in settings.TRUSTED_OP_LIST])


async def get_user(
    session: Session = Depends(db.get_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> models.User:
    token_info = flaat.get_user_infos_from_access_token(token.credentials)
    subiss = token_info.subject, token_info.issuer
    return crud.user.get(session, id=subiss)
