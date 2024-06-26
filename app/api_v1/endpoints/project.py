"""Endpoints for the project generation from the cookiecutter template."""

# pylint: disable=unused-argument,missing-module-docstring
import logging
import shutil
import tempfile
from uuid import UUID

from cookiecutter.main import cookiecutter
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app import authentication, database, models, utils
from app.api_v1 import parameters, schemas
from app.api_v1.schemas import Input

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    summary="(Public) Fetches fields of the cookiecutter template.",
    operation_id="fetchFields",
    path="/{uuid}",
    responses={
        status.HTTP_200_OK: {
            "description": "Fields Fetched Successfully",
            "model": schemas.CutterForm,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Template Not Found",
            "model": schemas.NotFound,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Unprocessable Content",
            "model": schemas.Unprocessable,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
            "model": schemas.ServerError,
        },
        status.HTTP_501_NOT_IMPLEMENTED: {
            "description": "Not Implemented Error",
            "model": schemas.NotImplemented,
        },
    },
    status_code=status.HTTP_200_OK,
    response_model=schemas.CutterForm,
)
async def fetch_fields(
    *,
    session: Session = Depends(database.get_session),
    uuid: UUID = parameters.template_uuid,
) -> list[dict]:
    """
    Use this method to fetch fields of the cookiecutter template to build the
    web form.
    """

    logger.info("Fetching fields of the cookiecutter template.")
    logger.debug("Fetching template with id: %s.", uuid)
    template = session.get(models.Template, uuid)

    logger.debug("Checking if template exists.")
    if not template:
        raise NoResultFound("Template not found")

    logger.debug("Fetching cookiecutter.json file.")
    data = utils.fetch_arguments(template)

    logger.debug("Returning CutterForm dict from json")
    return utils.parse_fields(data)


@router.post(
    summary="(User) Generate software project from the template.",
    operation_id="generateProject",
    path="/{uuid}:generate",
    responses={
        status.HTTP_200_OK: {
            "description": "Project Generated Successfully",
            "content": {"application/zip": {"schema": {"type": "string", "format": "binary"}}},
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticated",
            "model": schemas.Unauthorized,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Template Not Found",
            "model": schemas.NotFound,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Unprocessable Content",
            "model": schemas.Unprocessable,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
            "model": schemas.ServerError,
        },
    },
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
)
async def generate_project(
    *,
    session: Session = Depends(database.get_session),
    tempdir: tempfile.TemporaryDirectory = Depends(utils.temp_folder),
    uuid: UUID = parameters.template_uuid,
    options_in: dict[str, Input] = Body(),
    current_user: models.User = Depends(authentication.get_user),
) -> FileResponse:
    """
    Use this method to generate software project using the specific template.
    Generated project is returned as `.zip` file.
    """

    logger.info("Generating software project from the template.")
    logger.debug("Fetching template with id: %s.", uuid)
    template = session.get(models.Template, uuid)

    logger.debug("Checking if template exists.")
    if not template:
        raise NoResultFound("Template not found")

    logger.debug("Parse boolean fields into cookiecutter format.")
    data = utils.fetch_arguments(template)
    bool_fields = [k for k, v in data.items() if isinstance(v, bool)]
    for key in filter(lambda k: k in options_in, bool_fields):
        options_in[key] = utils.str2bool(options_in[key])

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
    return FileResponse(
        f"{tempdir}/project.zip",
        media_type="application/zip",
        filename="project.zip",
        headers={"Access-Control-Expose-Headers": "Content-Disposition"},
    )
