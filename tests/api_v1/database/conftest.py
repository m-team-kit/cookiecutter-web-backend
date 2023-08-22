import shutil
from unittest.mock import patch

import git
import pytest


@pytest.fixture(scope="module", autouse=True)
def patch_repository(request):
    """Patch fixture to set test env variables."""
    mock_repository = request.param if hasattr(request, "param") else "repository-1"
    clone_from = makecopy_repo(mock_repository)
    with patch.object(git.Repo, "clone_from", side_effect=clone_from):
        yield


def makecopy_repo(folder):
    """Make a copy generator of the target test mock repository."""
    # pylint: disable=unused-argument
    def patch_function(url, to_path, branch, depth):  # fmt: skip
        return shutil.copytree(f"tests/repositories/{folder}", to_path, dirs_exist_ok=True)
    return patch_function
