# pylint: disable=unused-argument
import logging
from typing import List
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependencies as deps

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    summary="(Public) Lists available templates.",
    operation_id="listTemplates",
    path="/",
    responses={
        status.HTTP_200_OK: {"model": schemas.Template},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.SearchError},
    },
    response_model=List[schemas.Template],
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
    summary="(Public) Finds template by UUID and shows its details.",
    operation_id="getTemplate",
    path="/{uuid}",
    responses={
        status.HTTP_200_OK: {"model": schemas.Template},
        status.HTTP_404_NOT_FOUND: {"description": "Template not found"},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.GetError},
    },
    response_model=schemas.Template,
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
    summary="(User) Rates specific template.",
    operation_id="rateTemplate",
    path="/{uuid}/score",
    responses={
        status.HTTP_200_OK: {"model": schemas.Template},
        status.HTTP_201_CREATED: {"model": schemas.Template},
        status.HTTP_404_NOT_FOUND: {"description": "Template not found"},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.ScoreError},
    },
    response_model=schemas.Template,
)
def rate_template(
    response: Response,
    uuid: UUID,
    score: float = Body(),
    current_user: models.User = Depends(deps.get_user),
    session: Session = Depends(deps.get_session),
) -> models.Template:
    """
    Use this method to update the score/rating of the specific template.
    """

    logger.info("Rating template %s.", uuid)
    try:
        logger.debug("Getting template using crud template.")
        template = crud.template.get(session, id=uuid)

        logger.debug("Checking if template exists.")
        if not template:
            raise KeyError("Template not found")

        logger.debug("Calculate response depending if user already rated.")
        if (current_user.subject, current_user.issuer) in [x.owner_id for x in template.scores]:
            logger.debug("User already rated this template.")
            response.status_code = status.HTTP_200_OK
            logger.debug("Updating template with new score.")
            template = crud.template.update_rate(session, score, db_obj=template, user=current_user)
        else:
            logger.debug("User has not rated this template yet.")
            response.status_code = status.HTTP_201_CREATED
            logger.debug("Adding score to template.")
            template = crud.template.add_rate(session, score, db_obj=template, user=current_user)

        logger.debug("Returning template.")
        response.headers["Location"] = f"/api/v1/templates/{template.id}"
        return template

    except KeyError as err:
        logger.debug("Template %s not found: %s", uuid, err)
        raise HTTPException(status_code=404, detail=err.args[0]) from err

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error rating template %s: %s", uuid, err)
        raise HTTPException("Server error")
