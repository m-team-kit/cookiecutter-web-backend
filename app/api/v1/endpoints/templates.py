from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app import crud, db, models, schemas
from app.core import authentication as auth

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Template],
    summary="(Public) Lists available templates.",
    operation_id="listTemplates",
)
def read_templates(
    *,
    session: Session = Depends(db.get_session),
) -> List[models.Template]:
    """
    Use this method to get a list of available templates. The response
    returns a pagination object with the templates.
    """
    try:
        templates = crud.template.get_multi(session)
        return templates
    except Exception as e:  # TODO: Too broad exception
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    path="/{uuid}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Template not found"}},
    response_model=schemas.Template,
    summary="(Public) Finds template by UUID and shows its details.",
    operation_id="getTemplate",
)
def read_template(
    *,
    session: Session = Depends(db.get_session),
    uuid: UUID,
) -> models.Template:
    """
    Use this method to retrieve details about the specific template.
    """
    template = crud.template.get(session, id=uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put(
    path="/{uuid}/score",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Template not found"}},
    response_model=schemas.Template,
    summary="(User) Rates specific template.",
    operation_id="rateTemplate",
)
def rate_template(
    *,
    session: Session = Depends(db.get_session),
    uuid: UUID,
    score: float = Body(),
    current_user: models.User = Depends(auth.get_user),
) -> models.Template:
    """
    Use this method to update the score/rating of the specific template.
    """
    template = crud.template.get(session, id=uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    template.score(score, db=session, user=current_user)
    return template
