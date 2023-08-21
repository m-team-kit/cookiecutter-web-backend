# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
import pytest


@pytest.fixture(scope="package")
def api_url():
    """Return the API URL."""
    return "/api/v1"
