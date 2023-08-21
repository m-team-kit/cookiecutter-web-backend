# pylint: disable=redefined-outer-name
from typing import Dict
import pytest
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def response(client: TestClient, headers: Dict) -> None:
    """Performs a POST request to create a database."""
    response = client.post("/api/v1/db:create", headers=headers)
    return response


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_HTTP_200_OK(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    assert response.json() == {}  # TODO: Fix response


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer bad-secret"}], indirect=True)
def test_HTTP_401_UNAUTHORIZED(response: Response) -> None:
    """Tests the response status code is 401 and valid."""
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect secret"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{}], indirect=True)
def test_HTTP_403_UNAUTHORIZED(response: Response) -> None:
    """Tests the response status code is 403 and valid."""
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
