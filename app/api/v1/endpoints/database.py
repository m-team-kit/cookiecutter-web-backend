from fastapi import APIRouter, Depends, status

from app import models
from app.api import dependencies as deps

router = APIRouter()


@router.post(
    path=":create",
    status_code=204,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    summary="(Admin) Creates local database.",
    operation_id="createDB",
)
def create_database(
    valid_secret: models.User = Depends(deps.check_secret),
) -> None:
    """
    Use this method to create local copy of the database from YAML files in
    the git repository.
    """
    raise NotImplementedError


@router.post(
    path=":update",
    status_code=204,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    summary="(Admin) Updates local database.",
    operation_id="updateDB",
)
def update_database(
    valid_secret: models.User = Depends(deps.check_secret),
) -> None:
    """
    Use this method to update local copy of the database from YAML files in
    the git repository.
    """
    raise NotImplementedError
