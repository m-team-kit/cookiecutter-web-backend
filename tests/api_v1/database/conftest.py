import pytest


@pytest.fixture(scope="package")
def api_secret(request, environment: dict):
    """Return the API secret."""
    if "param" in request:
        return request.param
    return environment["API_SECRET"]
