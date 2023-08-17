from fastapi import APIRouter, Depends

from app import models
from app.api import deps

router = APIRouter()


@router.post(
    path=":create",
    status_code=204,
    summary="(Admin) Creates local database.",
    operation_id="createDB",
)
def create_database(
    current_user: models.User = Depends(deps.get_user),
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
    current_user: models.User = Depends(deps.get_user),
) -> None:
    """
    Use this method to update local copy of the database from YAML files in
    the git repository.
    """
    raise NotImplementedError
