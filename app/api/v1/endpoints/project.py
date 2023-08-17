from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    path="/{uuid}",
    response_model=List[schemas.Option],
    summary="(Public) Fetches fields of the cookiecutter template.",
    operation_id="fetchFields",
)
def options_project(
    *,
    database: Session = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    """
    Use this method to fetch fields of the cookiecutter template to build the
    web form.
    """
    template = crud.template.get(db=database, id=uuid)
    return template.options


@router.post(
    path="/{uuid}:generate",
    response_model=schemas.Project,
    summary="(User) Generate software project from the template.",
    operation_id="createProject",
)
def generate_project(
    *,
    database: Session = Depends(deps.get_db),
    uuid: UUID,
    options_in: List[schemas.Option],
    current_user: models.User = Depends(deps.get_user),
) -> Any:
    """
    Use this method to generate software project using the specific template.
    Generated project is returned as `.zip` file.
    """
    template = crud.template.get(db=database, id=uuid)
    return template.project(owner_id=current_user.id, options=options_in)
