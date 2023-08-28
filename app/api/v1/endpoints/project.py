# pylint: disable=unused-argument
import io
import json
import logging
import shutil
import tempfile
import urllib.request
from typing import Any, Dict
from uuid import UUID

from cookiecutter.main import cookiecutter
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies as deps

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    summary="(Public) Fetches fields of the cookiecutter template.",
    operation_id="fetchFields",
    path="/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    responses={
        status.HTTP_200_OK: {"model": Dict[str, Any]},
        status.HTTP_404_NOT_FOUND: {"description": "Template not found"},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.SearchError},
    },
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

    logger.info("Fetching fields of the cookiecutter template.")
    try:
        logger.debug("Fetching template with id: %s.", uuid)
        template = crud.template.get(session, id=uuid)

        logger.debug("Checking if template exists.")
        if not template:
            raise KeyError("Template not found")

        logger.debug("Fetching cookiecutter.json file.")
        url = f"{template.gitLink}/raw/{template.gitCheckout}/cookiecutter.json"
        req = urllib.request.Request(url)

        logger.debug("Returning cookiecutter.json file.")
        return json.load(urllib.request.urlopen(req))

    except KeyError as err:
        logger.debug("Template %s not found: %s", uuid, err)
        raise HTTPException(status_code=404, detail=err.args[0]) from err

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error getting template %s: %s", uuid, err)
        raise HTTPException("Server error") from err


@router.post(
    summary="(User) Generate software project from the template.",
    operation_id="createProject",
    path="/{uuid}:generate",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    responses={200: {"content": {"application/zip": {}}}},
)
def generate_project(
    *,
    session: Session = Depends(deps.get_session),
    uuid: UUID,
    options_in: Dict[str, str] = Body(),
    current_user: models.User = Depends(deps.get_user),
) -> StreamingResponse:
    """
    Use this method to generate software project using the specific template.
    Generated project is returned as `.zip` file.
    """

    logger.info("Generating software project from the template.")
    try:
        logger.debug("Fetching template with id: %s.", uuid)
        template = crud.template.get(session, id=uuid)

        logger.debug("Checking if template exists.")
        if not template:
            raise KeyError("Template not found")

        logger.debug("Generating project into memory zip.")
        project = create_project(template.gitLink, template.gitCheckout, options_in)

        logger.debug("Returning cookiecutter.json file.")
        return StreamingResponse(project, media_type="application/zip")

    except KeyError as err:
        logger.debug("Template %s not found: %s", uuid, err)
        raise HTTPException(status_code=404, detail=err.args[0]) from err

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error getting template %s: %s", uuid, err)
        raise HTTPException("Server error") from err


def create_project(url, checkout, options_in):
    """Generate a project from a cookiecutter template and return it as a zip file."""
    with tempfile.TemporaryDirectory() as tempdir:
        cookiecutter(url, checkout, no_input=True, extra_context=options_in, output_dir=f"{tempdir}/project")
        shutil.make_archive(f"{tempdir}/project", "zip", f"{tempdir}/project", logger=logger)
        with open(f"{tempdir}/project.zip", "rb") as zip_file:
            zip_contents = zip_file.read()
        return io.BytesIO(zip_contents)
