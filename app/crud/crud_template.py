from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate


class CRUDTemplate(CRUDBase[Template, TemplateCreate, TemplateUpdate]):
    def create_with_owner(
        self, session: Session, *, obj_in: TemplateCreate, owner_id: int
    ) -> Template:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, session: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Template]:
        return (
            session.query(self.model)
            .filter(Template.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


template = CRUDTemplate(Template)
