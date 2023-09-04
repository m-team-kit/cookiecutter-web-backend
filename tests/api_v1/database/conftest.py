# pylint: disable=unused-argument
import shutil
from unittest.mock import patch

import git
import pytest
from git import InvalidGitRepositoryError


@pytest.fixture(scope="module", params=[])
def patch_repository(request):
    """Patch fixture to replace request response from repository with data."""
    patch_function = clone_patch_gen(request.param)
    with patch.object(git.Repo, "clone_from", side_effect=patch_function):
        yield


def clone_patch_gen(reposirtory_folder):
    def clone_patch(url, to_path, branch, depth):  # fmt: skip
        """Patch fixture that copies repository files into destination."""
        try:
            repo_folder = f"tests/repositories/{reposirtory_folder}"
            return shutil.copytree(repo_folder, to_path, dirs_exist_ok=True)
        except FileNotFoundError as err:
            raise InvalidGitRepositoryError(reposirtory_folder) from err
    return clone_patch
