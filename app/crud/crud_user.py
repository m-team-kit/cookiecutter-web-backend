from typing import Any, Dict, Optional, Tuple, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

Subject = str
Issuer = str


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get(
            self, session: Session, *, id: Tuple[Subject, Issuer]
    ) -> Optional[User]:
        return (
            session.query(User)
            .filter(User.issuer == id[1])
            .filter(User.subject == id[0])
            .first()
        )

    def create(
            self, session: Session, *, id: Tuple[Subject, Issuer]
    ) -> User:
        db_obj = User(subject=id[0], issuer=id[1])
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
            self, session: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        raise NotImplementedError("No user data is stored in the database.")

    def remove(
            self, session: Session, id: Tuple[Subject, Issuer]
    ) -> Optional[User]:
        obj = self.get(session, id=id)
        session.delete(obj)
        session.commit()
        return obj


user = CRUDUser(User)
