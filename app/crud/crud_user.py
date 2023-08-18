from app.crud.base import CRUDToken
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDToken[User, UserCreate, UserUpdate]):
    pass


user = CRUDUser(User)
