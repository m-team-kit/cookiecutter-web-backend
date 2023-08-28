# pylint: disable=redefined-outer-name
from typing import Any, Dict
import zipfile
import io

import pytest
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def response(client: TestClient, template_uuid: str, headers: Dict, body: Dict) -> None:
    """Performs a POST request to create a database."""
    response = client.post(f"/api/v1/project/{template_uuid}:generate", json=body, headers=headers)
    return response


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [{"directory_name": "my_project"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_200_ok(response: Response, body: Dict[str, Any]) -> None:
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert header is valid
    assert response.headers["content-type"] == "application/zip"
    # Assert template in response is valid
    zip_buffer = io.BytesIO(response.content)
    directory_name = body.get("directory_name", "Hello")
    file_name = body.get("file_name", "Howdy")
    with zipfile.ZipFile(zip_buffer, "r", zipfile.ZIP_DEFLATED, False) as zip_ref:
        assert zip_ref.namelist() == [f"{directory_name}/", f"{directory_name}/{file_name}.py"]


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [{"directory_name": "my_project"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer bad-token"}, {}], indirect=True)
def test_401_unauthorized(response: Response) -> None:
    """Tests the response status code is 401 and valid."""
    # Assert response is valid
    assert response.status_code == 401
    # Assert header is valid
    assert response.headers["WWW-Authenticate"] == "Bearer"
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Not authenticated"}


@pytest.mark.parametrize("template_uuid", ["unknown"], indirect=True)
@pytest.mark.parametrize("body", [{"directory_name": "my_project"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_404_not_found(response: Response) -> None:
    """Tests the response status code is 404 and valid."""
    # Assert response is valid
    assert response.status_code == 404
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Template not found"}


@pytest.mark.parametrize("template_uuid", ["bad_uuid"], indirect=True)
@pytest.mark.parametrize("body", [{"directory_name": "my_project"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
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
