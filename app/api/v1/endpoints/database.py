from fastapi import APIRouter, Depends

from app import models
from app.core import authentication as auth

router = APIRouter()


@router.post(
    path=":create",
    status_code=204,
    summary="(Admin) Creates local database.",
    operation_id="createDB",
)
def create_database(
    current_user: models.User = Depends(auth.get_user),
) -> None:
    """
    Use this method to create local copy of the database from YAML files in
    the git repository.
    """
    raise NotImplementedError


@router.post(
    path=":update",
    status_code=204,
    summary="(Admin) Updates local database.",
    operation_id="updateDB",
)
def update_database(
    current_user: models.User = Depends(auth.get_user),
) -> None:
    """
    Use this method to update local copy of the database from YAML files in
    the git repository.
    """
    raise NotImplementedError
