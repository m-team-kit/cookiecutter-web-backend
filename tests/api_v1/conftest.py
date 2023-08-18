import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client(environment):
    """Import application interface for the tests."""
    from app.__main__ import api_v1  # fmt: skip
    return TestClient(api_v1)
