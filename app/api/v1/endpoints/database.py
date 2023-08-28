# pylint: disable=unused-argument
import json
import logging
import pathlib
import tempfile

import git
from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies as deps

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    summary="(Admin) Creates local database.",
    operation_id="createDB",
    path=":create",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Database created."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error."},
    },
)
def create_database(
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

    try:
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
            create_template(session, path)

    except Exception as err:  # TODO: Too generic exception
        logger.error("Error creating local database: %s", err)
        raise HTTPException("Server error") from err


@router.post(
    summary="(Admin) Updates local database.",
    operation_id="updateDB",
    path=":update",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Database updated."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error."},
    },
)
def update_database(
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

    try:
        logger.debug("Cloning repository at %s.", tempdir)
        git.Repo.clone_from(
            url=f"{request.app.state.settings.repository_url}",
            to_path=tempdir,
            branch="main",
            depth=1,
        )

        logger.debug("Collect all templates from database.")
        templates = crud.template.get_multi(session, limit=None)
        temp_files = [x.repoFile for x in templates]

        logger.debug("Collecting all json from repository.")
        repo_files = [x.name for x in pathlib.Path(tempdir).glob("*.json")]

        logger.debug("Delete difference between database and repository.")
        to_delete = set(temp_files) - set(repo_files)
        for template in [x for x in templates if x.repoFile in to_delete]:
            crud.template.remove(session, id=template.id)

        logger.debug("Creating templates from json files.")
        to_create = set(repo_files) - set(temp_files)
        for repo_file in [x for x in repo_files if x in to_create]:
            create_template(session, pathlib.Path(tempdir) / repo_file)

        logger.debug("Updating templates from json files.")
        to_update = set(temp_files) - set(to_delete)
        for template in [x for x in templates if x.repoFile in to_update]:
            update_template(session, template, pathlib.Path(tempdir))

    except Exception as err:  # TODO: Too generic exception
        logger.error("Error updating local database: %s", err)
        raise HTTPException("Server error") from err


def create_template(session: Session, repo_file: pathlib.Path) -> None:
    logger.debug("Opening template file for %s.", repo_file)
    with open(repo_file, "r", encoding="utf-8") as file:
        template_kwds = json.load(file)
        template_kwds["repoFile"] = repo_file.name
        logger.debug("Creating template %s.", template_kwds)
        crud.template.create(session, obj_in=template_kwds)


def update_template(session: Session, template: models.Template, dir: pathlib.Path) -> None:
    logger.debug("Opening template file for %s.", template.repoFile)
    with open(dir / template.repoFile, "r", encoding="utf-8") as file:
        template_kwds = json.load(file)
        logger.debug("Updating template %s.", template_kwds)
        crud.template.update(session, db_obj=template, obj_in=template_kwds)
