from fastapi import Depends
from fastapi.security import HTTPBearer
from flaat.fastapi import Flaat
from sqlalchemy.orm import Session

from app import db
from app.core.config import settings

bearer_token = HTTPBearer()
flaat = Flaat()
flaat.set_trusted_OP_list([str(x) for x in settings.TRUSTED_OP_LIST])


async def get_user(
    session: Session = Depends(db.get_session),
    token: str = Depends(bearer_token),
) -> str:  # models.User:
    token_info = flaat.get_user_infos_from_access_token(token.credentials)
    subiss = (token_info.subject, token_info.issuer)
    # db_user = crud.user.get(db=session, id=subiss)
    return subiss
