from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Template, Score
from app.schemas.template import TemplateCreate, TemplateUpdate
from app.schemas.user import User


class CRUDTemplate(CRUDBase[Template, TemplateCreate, TemplateUpdate]):
    def add_rate(self, session: Session, score: int, *, db_obj: Template, user: User) -> Template:
        """Adds a Score from user to the template."""
        score = Score(owner_subject=user.subject, owner_issuer=user.issuer, value=score)
        db_obj.scores.append(score)
        session.add(user)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update_rate(self, session: Session, score: int, *, db_obj: Template, user: User) -> Template:
        """Updates a Score from user to the template."""
        for score_item in db_obj.scores:
            if score_item.owner_id == (user.subject, user.issuer):
                score_item.value = score
                break
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


template = CRUDTemplate(Template)
