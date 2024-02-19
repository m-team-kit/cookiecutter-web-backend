"""Endpoints for creating and updating local database from git repository."""

# pylint: disable=unused-argument,missing-module-docstring
import json
import logging
import pathlib
import tempfile

import git
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import authentication, config, database, models, notifications, utils
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
    tempdir: tempfile.TemporaryDirectory = Depends(utils.temp_folder),
    valid_secret: models.User = Depends(authentication.check_secret),
    session: Session = Depends(database.get_session),
    settings: database.Settings = Depends(config.get_settings),
    notification: None = Depends(notifications.db_created),
) -> None:
    """
    Use this method to create local copy of the database from YAML files in
    the git repository.
    """
    # pylint: disable=consider-using-with

    logger.info("Creating local database.")
    logger.debug("Cloning repository at %s.", tempdir)
    git.Repo.clone_from(f"{settings.repository_url}", tempdir, branch="main", depth=1)

    logger.debug("Deleting all templates, tags and users from database.")
    session.query(models.Template).delete()
    session.query(models.Tag).delete()
    session.query(models.User).delete()

    logger.debug("Creating templates from json files.")
    for path in pathlib.Path(tempdir).glob("*.json"):
        _create_template(session, path)

    logger.debug("Commit changes to database.")
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
    tempdir: tempfile.TemporaryDirectory = Depends(utils.temp_folder),
    valid_secret: models.User = Depends(authentication.check_secret),
    session: Session = Depends(database.get_session),
    settings: database.Settings = Depends(config.get_settings),
    notification: None = Depends(notifications.db_updated),
) -> None:
    """
    Use this method to update local copy of the database from YAML files in
    the git repository.
    """
    # pylint: disable=consider-using-with

    logger.info("Creating local database.")
    logger.debug("Cloning repository at %s.", tempdir)
    git.Repo.clone_from(f"{settings.repository_url}", tempdir, branch="main", depth=1)

    logger.debug("Delete all tags from database.")
    session.query(models.Tag).delete()

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

    logger.debug("Delete all users that do not have any scores.")
    session.flush()
    session.query(models.User).filter(~models.User.scores.any()).delete()

    logger.debug("Commit changes to database.")
    session.commit()


def _create_template(session: Session, repo_file: pathlib.Path) -> None:
    logger.debug("Opening template file for %s.", repo_file)
    with open(repo_file, "r", encoding="utf-8") as file:
        template_kwds = json.load(file)
        template_kwds["repoFile"] = repo_file.name
        logger.debug("Creating template %s.", template_kwds)
        session.add(models.Template(**template_kwds))


def _update_template(session: Session, template: models.Template, dir: pathlib.Path) -> None:
    logger.debug("Opening template file for %s.", template.repoFile)
    with open(dir / template.repoFile, "r", encoding="utf-8") as file:
        template_kwds = json.load(file)
        logger.debug("Updating template %s.", template_kwds)
        for key, value in template_kwds.items():
            setattr(template, key, value)
        template.score = utils.calculate_score(template.scores)
        session.add(template)
