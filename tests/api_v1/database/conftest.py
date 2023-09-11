# pylint: disable=missing-module-docstring,unused-argument
import shutil
from pathlib import Path
from unittest.mock import patch

import git
import pytest
from git import InvalidGitRepositoryError

from app import models


@pytest.fixture(scope="module")
def templates(response, sql_session):
    """Fixture to provide database templates after request."""
    templates = sql_session.query(models.Template).all()
    yield {Path(t.repoFile).stem: t for t in templates}


@pytest.fixture(scope="module")
def notifications(response):
    """Fixture to return notifications."""
    raise NotImplementedError  # TODO: Implement


@pytest.fixture(scope="module")
def patch_repository(request):
    """Patch fixture to replace request response from repository with data."""
    if hasattr(request, "param"):
        patch_function = clone_patch_gen(request.param)
        with patch.object(git.Repo, "clone_from", side_effect=patch_function):
            yield
    else:
        yield


def clone_patch_gen(repository_folder):
    """Patch fixture to replace request response from repository with data."""
    def clone_patch(url, to_path, branch, depth):  # fmt: skip
        """Patch fixture that copies repository files into destination."""
        try:
            repo_folder = f"tests/repositories/{repository_folder}"
            return shutil.copytree(repo_folder, to_path, dirs_exist_ok=True)
        except FileNotFoundError as err:
            raise InvalidGitRepositoryError(repository_folder) from err
    return clone_patch
