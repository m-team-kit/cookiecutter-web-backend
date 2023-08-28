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
from fastapi.responses import FileResponse
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
def fetch_fields(
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
    operation_id="generateProject",
    path="/{uuid}:generate",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    responses={
        status.HTTP_200_OK: {"content": {"application/zip": {}}},
        status.HTTP_404_NOT_FOUND: {"description": "Template not found"},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.SearchError},
    },
)
def generate_project(
    *,
    session: Session = Depends(deps.get_session),
    tempdir: tempfile.TemporaryDirectory = Depends(deps.temp_folder),
    uuid: UUID,
    options_in: Dict[str, str] = Body(),
    current_user: models.User = Depends(deps.get_user),
) -> FileResponse:
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
        cookiecutter(
            template=template.gitLink,
            checkout=template.gitCheckout,
            no_input=True,
            extra_context=options_in,
            output_dir=f"{tempdir}/project",
        )

        logger.debug("Creating zip file from project folder.")
        shutil.make_archive(f"{tempdir}/project", "zip", f"{tempdir}/project", logger=logger)

        logger.debug("Returning cookiecutter.json file.")
        return FileResponse(f"{tempdir}/project.zip", media_type="application/zip", filename="project.zip")

    except KeyError as err:
        logger.debug("Template %s not found: %s", uuid, err)
        raise HTTPException(status_code=404, detail=err.args[0]) from err

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error getting template %s: %s", uuid, err)
        raise HTTPException("Server error") from err
