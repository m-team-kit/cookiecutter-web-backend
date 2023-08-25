from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies as deps

router = APIRouter()


@router.get(
    summary="(Public) Fetches fields of the cookiecutter template.",
    operation_id="fetchFields",
    path="/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    responses={},
)
def options_project(
    *,
    session: Session = Depends(deps.get_session),
    uuid: UUID,
) -> Dict[str, Any]:
    """
    Use this method to fetch fields of the cookiecutter template to build the
    web form.
    """
    template = crud.template.get(session, id=uuid)
    return template.options


@router.post(
    summary="(User) Generate software project from the template.",
    operation_id="createProject",
    path="/{uuid}:generate",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    responses={200: {"content": {"application/zip": {}}}},
)
def generate_project(
    *,
    session: Session = Depends(deps.get_session),
    uuid: UUID,
    options_in: Dict[str, str] = Body(),
    current_user: models.User = Depends(deps.get_user),
) -> FileResponse:
    """
    Use this method to generate software project using the specific template.
    Generated project is returned as `.zip` file.
    """
    # template = crud.template.get(db=session, id=uuid)
    # return template.project(owner_id=current_user.id, options=options_in)
    return FileResponse("favicon.ico", media_type="image/vnd.microsoft.icon")
