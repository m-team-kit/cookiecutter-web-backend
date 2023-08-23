# pylint: disable=unused-argument
import shutil
from unittest.mock import patch

import git
import pytest


@pytest.fixture(scope="module", autouse=True)
def patch_repository():
    """Patch fixture to set test env variables."""
    with patch.object(git.Repo, "clone_from", side_effect=clone_patch):
        yield


def clone_patch(url, to_path, branch, depth):
    """Patch fixture that copies repository files into destination."""
    return shutil.copytree("tests/repository", to_path, dirs_exist_ok=True)
