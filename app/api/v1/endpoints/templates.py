from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app import crud, db, models, schemas
from app.core import authentication as auth

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="(Public) Lists available templates.",
    operation_id="listTemplates",
)
def read_templates(
    *,
    session: Session = Depends(db.get_session),
) -> List[schemas.Template]:
    """
    Use this method to get a list of available templates. The response
    returns a pagination object with the templates.
    """
    templates = crud.template.get_multi(db=session)
    return templates


@router.get(
    path="/{uuid}",
    status_code=status.HTTP_200_OK,
    summary="(Public) Finds template by UUID and shows its details.",
    operation_id="getTemplate",
)
def read_template(
    *,
    session: Session = Depends(db.get_session),
    uuid: UUID,
) -> schemas.Template:
    """
    Use this method to retrieve details about the specific template.
    """
    template = crud.template.get(db=session, id=uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put(
    path="/{uuid}/score",
    status_code=status.HTTP_200_OK,
    summary="(User) Rates specific template.",
    operation_id="rateTemplate",
)
def rate_template(
    *,
    session: Session = Depends(db.get_session),
    uuid: UUID,
    score: float = Body(),
    current_user: models.User = Depends(auth.get_user),
) -> schemas.Template:
    """
    Use this method to update the score/rating of the specific template.
    """
    template = crud.template.get(db=session, id=uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    template.score(score, db=session, user=current_user)
    return template
