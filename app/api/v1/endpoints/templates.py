from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    path="/",
    response_model=List[schemas.Template],
    summary="(Public) Lists available templates.",
    operation_id="listTemplates",
)
def read_templates(
    database: Session = Depends(deps.get_db),
) -> Any:
    """
    Use this method to get a list of available templates. The response
    returns a pagination object with the templates.
    """
    templates = crud.template.get_multi(db=database)
    return templates


@router.get(
    path="/{uuid}",
    response_model=schemas.Template,
    summary="(Public) Finds template by UUID and shows its details.",
    operation_id="getTemplate",
)
def read_template(
    *,
    database: Session = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    """
    Use this method to retrieve details about the specific template.
    """
    template = crud.template.get(db=database, id=uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put(
    path="/{uuid}/score",
    response_model=schemas.Template,
    summary="(User) Rates specific template.",
    operation_id="rateTemplate",
)
def update_template(
    *,
    database: Session = Depends(deps.get_db),
    uuid: UUID,
    template_in: schemas.TemplateUpdate,
    current_user: models.User = Depends(deps.get_user),
) -> Any:
    """
    Use this method to update the score/rating of the specific template.
    """
    template = crud.template.get(db=database, id=uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if not crud.user.is_superuser(current_user) and (template.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    template = crud.template.update(db=database, db_obj=template, obj_in=template_in)
    return template
