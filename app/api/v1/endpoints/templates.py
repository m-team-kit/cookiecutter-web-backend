# pylint: disable=unused-argument
import logging
from typing import List
from uuid import UUID

import sqlalchemy as sa

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependencies as deps

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Template],
    summary="(Public) Lists available templates.",
    operation_id="listTemplates",
)
def read_templates(
    language: str = Query(default=None, description="Language of the template."),
    tags: List[str] = Query(default=[], description="Tags of the template."),
    keywords: List[str] = Query(default=[], description="Keywords of the template."),
    session: Session = Depends(deps.get_session),
) -> List[models.Template]:
    """
    Use this method to get a list of available templates. The response
    returns a pagination object with the templates.
    """

    logger.info("Listing templates.")
    search = session.query(models.Template)

    try:
        logger.debug("Filtering templates by language: %s.", language)
        if language:
            search = search.filter(models.Template.language == language)

        logger.debug("Filtering templates by keywords: %s.", keywords)
        for keyword in keywords:
            search = search.filter(
                sa.or_(
                    models.Template.title.contains(keyword),
                    models.Template.summary.contains(keyword),
                )
            )

        logger.debug("Filtering templates by tags: %s.", tags)
        search = search.join(models.Template._tags)
        search = search.filter(models.Tag.name.in_(tags))
        search = search.group_by(models.Template.id)
        search = search.having(sa.func.count(models.Tag.id) == len(tags))

        logger.debug("Returning templates.")
        return search.all()

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error listing templates: %s", err)
        raise HTTPException("Server error")


@router.get(
    path="/{uuid}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Template not found"}},
    response_model=schemas.Template,
    summary="(Public) Finds template by UUID and shows its details.",
    operation_id="getTemplate",
)
def read_template(
    uuid: UUID,
    session: Session = Depends(deps.get_session),
) -> models.Template:
    """
    Use this method to retrieve details about the specific template.
    """

    logger.info("Getting template %s.", uuid)
    try:
        logger.debug("Getting template using crud template.")
        template = crud.template.get(session, id=uuid)

        logger.debug("Checking if template exists.")
        if not template:
            raise KeyError("Template not found")

        logger.debug("Returning template.")
        return template

    except KeyError as err:
        logger.debug("Template %s not found: %s", uuid, err)
        raise HTTPException(status_code=404, detail=err.args[0]) from err

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error getting template %s: %s", uuid, err)
        raise HTTPException("Server error")


@router.put(
    path="/{uuid}/score",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Template not found"}},
    response_model=schemas.Template,
    summary="(User) Rates specific template.",
    operation_id="rateTemplate",
)
def rate_template(
    uuid: UUID,
    score: float = Body(),
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_user),
) -> models.Template:
    """
    Use this method to update the score/rating of the specific template.
    """
    template = crud.template.get(session, id=uuid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    template.score(score, db=session, user=current_user)
    return template
