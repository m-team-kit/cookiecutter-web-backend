# pylint: disable=unused-argument
import logging
from typing import List
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import dependencies as deps
from app import models
from app.api_v1 import parameters, schemas
from app.types import SortBy

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    summary="(Public) Lists available templates.",
    operation_id="listTemplates",
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Template],
    responses={
        status.HTTP_200_OK: {"model": List[schemas.Template]},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.ValidationError},
    },
)
def read_templates(
    session: Session = Depends(deps.get_session),
    language: str = parameters.language,
    tags: List[str] = parameters.tags,
    keywords: List[str] = parameters.keywords,
    sort_by: SortBy = parameters.sort_by,
) -> List[models.Template]:
    """
    Use this method to get a list of available templates. The response
    returns a pagination object with the templates.
    """

    logger.info("Listing templates with score average.")
    search = session.query(models.Template, sa.func.avg(models.Score.value).label("score"))
    search = search.outerjoin(models.Template.scores)
    search = search.group_by(models.Template.id)

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
        if tags:
            search = search.join(models.Template._tags)
            search = search.filter(models.Tag.name.in_(tags))
            search = search.group_by(models.Template.id)
            search = search.having(sa.func.count(models.Tag.id) == len(tags))

        logger.debug("Sorting templates by: %s.", sort_by)
        for sort in sort_by.split(","):
            if sort[0] == "-":
                search = search.order_by(sa.nullslast(sa.desc(sort[1:])))
            else:
                search = search.order_by(sa.nullslast(sa.asc(sort[1:])))

        logger.debug("Returning templates.")
        return [template for template, _ in search.all()]

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error listing templates: %s", err)
        raise HTTPException("Server error") from err


@router.get(
    summary="(Public) Finds template by UUID and shows its details.",
    operation_id="getTemplate",
    path="/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Template,
    responses={
        status.HTTP_200_OK: {"model": schemas.Template},
        status.HTTP_404_NOT_FOUND: {"model": schemas.NotFound},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.GetError},
    },
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
        logger.debug("Fetching template with id: %s.", uuid)
        template = session.get(models.Template, uuid)

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
        raise HTTPException("Server error") from err


@router.put(
    summary="(User) Rates specific template.",
    operation_id="rateTemplate",
    path="/{uuid}/score",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Template,
    responses={
        status.HTTP_200_OK: {"model": schemas.Template},
        status.HTTP_201_CREATED: {"model": schemas.Template},
        status.HTTP_404_NOT_FOUND: {"model": schemas.NotFound},
        # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.ScoreError},
    },
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
        logger.debug("Fetching template with id: %s.", uuid)
        template = session.get(models.Template, uuid)

        logger.debug("Checking if template exists.")
        if not template:
            raise KeyError("Template not found")

        logger.debug("Calculate response depending if user already rated.")
        for score_item in template.scores:
            if score_item.owner_id == (current_user.subject, current_user.issuer):
                logger.debug("User already rated this template.")
                response.status_code = status.HTTP_200_OK
                logger.debug("Updating template with new score.")
                score_item.value = score
                break
        else:
            logger.debug("User has not rated this template yet.")
            response.status_code = status.HTTP_201_CREATED
            logger.debug("Adding score to template.")
            score = models.Score(owner_subject=current_user.subject, owner_issuer=current_user.issuer, value=score)
            template.scores.append(score)
            session.add(template)

        logger.debug("Committing changes to database.")
        session.add(template)
        session.commit()

        logger.debug("Returning template.")
        response.headers["Location"] = f"/api/v1/templates/{template.id}"
        return template

    except KeyError as err:
        logger.debug("Template %s not found: %s", uuid, err)
        raise HTTPException(status_code=404, detail=err.args[0]) from err

    except Exception as err:  # TODO: Too broad exception
        logger.error("Error rating template %s: %s", uuid, err)
        raise HTTPException("Server error") from err
