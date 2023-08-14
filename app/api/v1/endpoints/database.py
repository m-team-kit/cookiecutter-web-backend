from fastapi import APIRouter, Depends

from app import models
from app.api import deps

router = APIRouter()


@router.post(
    path=":update",
    status_code=204,
    summary="(Admin) Updates local database.",
    operation_id="updateDatabase",
)
def update_database(
    repo: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> None:
    """
    Use this method to update local copy of the database from YAML files in
    the git repository.
    """
    raise NotImplementedError
