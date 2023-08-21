# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
import pytest
from fastapi.testclient import TestClient

from app import create_app


@pytest.fixture(scope="module")
def app(environment):
    """Generate application from factories model."""
    return create_app()


@pytest.fixture(scope="module")
def client(app):
    """Produce test client from application instance."""
    return TestClient(app)
