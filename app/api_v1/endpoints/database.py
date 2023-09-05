# pylint: disable=unused-argument,missing-module-docstring
import json
import logging
import pathlib
import tempfile

import git
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import models
from app.api_v1 import schemas

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    summary="(Admin) Creates local database.",
    operation_id="createDB",
    path=":create",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Database Created Successfully",
            "model": None,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not Authenticated",
            "model": schemas.Unauthorized,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not Authorized",
            "model": schemas.Forbidden,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
            "model": schemas.ServerError,
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def create_database(
    request: Request,
    tempdir: tempfile.TemporaryDirectory = Depends(deps.temp_folder),
    valid_secret: models.User = Depends(deps.check_secret),
    session: Session = Depends(deps.get_session),
) -> None:
    """
    Use this method to create local copy of the database from YAML files in
    the git repository.
    """
    # pylint: disable=consider-using-with

    logger.info("Creating local database.")
    logger.debug("Cloning repository at %s.", tempdir)
    git.Repo.clone_from(
        url=f"{request.app.state.settings.repository_url}",
        to_path=tempdir,
        branch="main",
        depth=1,
    )

    logger.debug("Deleting all templates from database.")
    session.query(models.Template).delete()

    logger.debug("Creating templates from json files.")
    for path in pathlib.Path(tempdir).glob("*.json"):
        _create_template(session, path)

    logger.debug("Committing changes to database.")
    session.commit()


@router.post(
    summary="(Admin) Updates local database.",
    operation_id="updateDB",
    path=":update",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Database Updated Successfully",
            "model": None,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not Authenticated",
            "model": schemas.Unauthorized,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not Authorized",
            "model": schemas.Forbidden,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
            "model": schemas.ServerError,
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def update_database(
    request: Request,
    tempdir: tempfile.TemporaryDirectory = Depends(deps.temp_folder),
    valid_secret: models.User = Depends(deps.check_secret),
    session: Session = Depends(deps.get_session),
) -> None:
    """
    Use this method to update local copy of the database from YAML files in
    the git repository.
    """
    # pylint: disable=consider-using-with

    logger.info("Creating local database.")
    logger.debug("Cloning repository at %s.", tempdir)
    git.Repo.clone_from(
        url=f"{request.app.state.settings.repository_url}",
        to_path=tempdir,
        branch="main",
        depth=1,
    )

    logger.debug("Collect all templates from database.")
    templates = session.query(models.Template).all()
    temp_files = [x.repoFile for x in templates]

    logger.debug("Collecting all json from repository.")
    repo_files = [x.name for x in pathlib.Path(tempdir).glob("*.json")]

    logger.debug("Delete difference between database and repository.")
    to_delete = set(temp_files) - set(repo_files)
    for template in [x for x in templates if x.repoFile in to_delete]:
        session.delete(template)

    logger.debug("Creating templates from json files.")
    to_create = set(repo_files) - set(temp_files)
    for repo_file in [x for x in repo_files if x in to_create]:
        _create_template(session, pathlib.Path(tempdir) / repo_file)

    logger.debug("Updating templates from json files.")
    to_update = set(temp_files) - set(to_delete)
    for template in [x for x in templates if x.repoFile in to_update]:
        _update_template(session, template, pathlib.Path(tempdir))

    logger.debug("Committing changes to database.")
    session.commit()


def _create_template(session: Session, repo_file: pathlib.Path) -> None:
    logger.debug("Opening template file for %s.", repo_file)
    with open(repo_file, "r", encoding="utf-8") as file:
        template_kwds = json.load(file)
        template_kwds["repoFile"] = repo_file.name
        logger.debug("Creating template %s.", template_kwds)
        session.add(models.Template(**template_kwds))


def _update_template(session: Session, template: models.Template, dir: pathlib.Path) -> None:
    # pylint: disable=redefined-builtin
    logger.debug("Opening template file for %s.", template.repoFile)
    with open(dir / template.repoFile, "r", encoding="utf-8") as file:
        template_kwds = json.load(file)
        logger.debug("Updating template %s.", template_kwds)
        for key, value in template_kwds.items():
            setattr(template, key, value)
        session.add(template)
