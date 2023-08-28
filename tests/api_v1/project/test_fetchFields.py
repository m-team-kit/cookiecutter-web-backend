# pylint: disable=redefined-outer-name
from typing import Dict

import pytest
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def response(client: TestClient, template_uuid: str, headers: Dict) -> None:
    """Performs a POST request to create a database."""
    response = client.get(f"/api/v1/project/{template_uuid}", headers=headers)
    return response


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_200_ok(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert template in response is valid
    message = response.json()
    assert message["directory_name"] == "Hello"
    assert message["file_name"] == "Howdy"
    assert message["greeting_recipient"] == "Julie"

@pytest.mark.parametrize("template_uuid", ["unknown"], indirect=True)
def test_404_not_found(response: Response) -> None:
    """Tests the response status code is 404 and valid."""
    # Assert response is valid
    assert response.status_code == 404
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Template not found"}


@pytest.mark.parametrize("template_uuid", ["bad_uuid"], indirect=True)
def test_422_validation_error(response: Response) -> None:
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]
    assert message["detail"][0]["input"] == "bad_uuid"
