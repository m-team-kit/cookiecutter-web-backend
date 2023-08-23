# pylint: disable=unused-argument
import json
import logging
import pathlib
import tempfile

import git
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies as deps

logger = logging.getLogger(__name__)
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
    logger.info("Creating local database.")
    logger.debug("Deleting all templates from database.")
    session.query(models.Template).delete()
    logger.debug("Creating temporary directory.")
    with tempfile.TemporaryDirectory() as tempdir:
        logger.debug("Cloning repository at %s.", tempdir)
        git.Repo.clone_from(
            url=f"{request.app.state.settings.repository_url}",
            to_path=tempdir,
            branch="main",
            depth=1,
        )
        logger.debug("Creating templates from json files.")
        for path in pathlib.Path(tempdir).glob("*.json"):
            logger.debug("Opening template file for %s.", path.name)
            with open(path, "r", encoding="utf-8") as file:
                template_kwds = json.load(file)
                template_kwds["repoFile"] = path.name
                logger.debug("Creating template %s.", template_kwds)
                crud.template.create(session, obj_in=template_kwds)
    logger.info("Local database created.")


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
