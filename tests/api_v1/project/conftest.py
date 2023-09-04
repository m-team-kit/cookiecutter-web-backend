# pylint: disable=unused-argument
import urllib.error
import urllib.request
from unittest.mock import MagicMock, patch
import app.api_v1.endpoints.project

import pytest


@pytest.fixture(scope="module", params=[])
def patch_fields_url(request):
    """Patch fixture to replace request response from cookiecutter.json."""
    with patch.object(urllib.request, "Request", MagicMock()):
        patch_function = urlopen_patch_gen(request.param)
        with patch.object(urllib.request, "urlopen", side_effect=patch_function):
            yield


def urlopen_patch_gen(folder):
    def urlopen_patch(req):  # fmt: skip
        """Patch fixture that returns tests/cookiecutter/cookiecutter.json."""
        try:
            with open(f"tests/cookiecutters/{folder}/cookiecutter.json", encoding="utf-8") as file:
                mock = MagicMock()
                mock.getcode.return_value = 200
                mock.read.return_value = file.read().encode()
                mock.__enter__.return_value = mock
                mock.return_value = mock
            return mock
        except FileNotFoundError as err:
            raise urllib.error.HTTPError(req.full_url, 404, "Not Found", None, None) from err
    return urlopen_patch


@pytest.fixture(scope="module", params=[])
def patch_cookiecutter(request):
    """Patch fixture to replace cookiecutter template from a link."""
    original_cookiecutter = app.api_v1.endpoints.project.cookiecutter
    with patch.object(app.api_v1.endpoints.project, "cookiecutter", MagicMock()) as mock:
        folder = f"tests/cookiecutters/{request.param}"
        mock.side_effect = cookiecutter_path_gen(folder, original_cookiecutter)
        yield


def cookiecutter_path_gen(folder, original):
    def cookiecutter_patch(template, checkout, **kwds):  # fmt: skip
        """Patch fixture that returns tests/cookiecutter/cookiecutter.json."""
        original(template=folder, **kwds)
    return cookiecutter_patch
