import json
import pathlib
import tempfile

import git
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies as deps

router = APIRouter()


@router.post(
    path=":create",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    summary="(Admin) Creates local database.",
    operation_id="createDB",
)
def create_database(
    request: Request,
    valid_secret: models.User = Depends(deps.check_secret),
    session: Session = Depends(deps.get_session),
) -> None:
    """
    Use this method to create local copy of the database from YAML files in
    the git repository.
    """
    # TODO: Delete all previous entries
    with tempfile.TemporaryDirectory() as tempdir:
        git.Repo.clone_from(
            url=f"{request.app.state.settings.repository_url}",
            to_path=tempdir,
            branch="main",
            depth=1,
        )
        for path in pathlib.Path(tempdir).glob("*.json"):
            with open(path, "r", encoding="utf-8") as file:
                template_kwds = json.load(file)
                template_kwds["repoFile"] = path.name
                crud.template.create(session, obj_in=template_kwds)
    return None


@router.post(
    path=":update",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    summary="(Admin) Updates local database.",
    operation_id="updateDB",
)
def update_database(
    request: Request,
    valid_secret: models.User = Depends(deps.check_secret),
    session: Session = Depends(deps.get_session),
) -> None:
    """
    Use this method to update local copy of the database from YAML files in
    the git repository.
    """
    raise NotImplementedError
