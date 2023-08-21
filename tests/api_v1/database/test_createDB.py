# pylint: disable=redefined-outer-name
import pytest
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def response(api_url: str, client: TestClient) -> None:
    """Performs a POST request to create a database."""
    response = client.post(f"{api_url}/db:create")
    return response


def test_HTTP_200_OK(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    assert response.json() == {"msg": "Database created successfully"}
