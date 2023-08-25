# pylint: disable=redefined-outer-name
from typing import Dict

import pytest
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def response(client: TestClient, template_uuid: str, headers: Dict, body: int) -> None:
    """Performs a POST request to create a database."""
    response = client.put(f"/api/v1/templates/{template_uuid}/score", content=body, headers=headers)
    return response


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [5], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "user_1-token"}], indirect=True)
def test_200_ok(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "bced037a-a326-425d-aa03-5d3cbc9aa3d1"
    assert message["repoFile"] == "my_template_1.json"
    assert message["title"] == "My Template 1"
    assert message["summary"] == "Template example 1"
    assert message["language"] == "Python"
    assert sorted(message["tags"]) == ["Tag1", "Tag2"]
    assert message["picture"] == "https://picture-url/template_1"
    assert message["gitLink"] == "https://some-git-link/template_1"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 5


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [5], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "user_1-token"}], indirect=True)
def test_201_created(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "bced037a-a326-425d-aa03-5d3cbc9aa3d1"
    assert message["repoFile"] == "my_template_1.json"
    assert message["title"] == "My Template 1"
    assert message["summary"] == "Template example 1"
    assert message["language"] == "Python"
    assert sorted(message["tags"]) == ["Tag1", "Tag2"]
    assert message["picture"] == "https://picture-url/template_1"
    assert message["gitLink"] == "https://some-git-link/template_1"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 5


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [5], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer bad-token"}], indirect=True)
def test_401_unauthorized(response: Response) -> None:
    """Tests the response status code is 401 and valid."""
    # Assert response is valid
    assert response.status_code == 401
    # Assert header is valid
    assert response.headers["WWW-Authenticate"] == "Bearer"
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Incorrect secret"}


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [5], indirect=True)
@pytest.mark.parametrize("headers", [{}], indirect=True)
def test_403_forbidden(response: Response) -> None:
    """Tests the response status code is 403 and valid."""
    # Asset response is valid
    assert response.status_code == 403
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Not authenticated"}


@pytest.mark.parametrize("template_uuid", ["unknown"], indirect=True)
@pytest.mark.parametrize("body", [5], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "user_1-token"}], indirect=True)
def test_404_not_found(response: Response) -> None:
    """Tests the response status code is 404 and valid."""
    # Assert response is valid
    assert response.status_code == 404
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Template not found"}


@pytest.mark.parametrize("template_uuid", ["bad_uuid"], indirect=True)
@pytest.mark.parametrize("body", [5], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "user_1-token"}], indirect=True)
def test_422_bad_uuid(response: Response) -> None:
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]
    assert message["detail"][0]["input"] == "bad_uuid"


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["a"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "user_1-token"}], indirect=True)
def test_422_bad_score(response: Response) -> None:
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]
    assert message["detail"][0]["input"] == "bad_uuid"
