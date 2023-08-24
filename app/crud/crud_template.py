from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Template
from app.schemas.template import TemplateCreate, TemplateUpdate


class CRUDTemplate(CRUDBase[Template, TemplateCreate, TemplateUpdate]):
    def create(self, session: Session, *, obj_in: TemplateCreate) -> Template:
        kwds = jsonable_encoder(obj_in)
        db_obj = Template(**kwds)  # type: ignore
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


template = CRUDTemplate(Template)
