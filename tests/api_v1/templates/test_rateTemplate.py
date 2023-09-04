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
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_200_updated_by_user_1(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "bced037a-a326-425d-aa03-5d3cbc9aa3d1"
    assert message["repoFile"] == "my_template_1.json"
    assert message["title"] == "My Template 1"
    assert message["summary"] == "Tests Cookiecutter"
    assert message["language"] == "Python"
    assert sorted(message["tags"]) == ["Tag1", "Tag2"]
    assert message["picture"] == "https://picture-url/template"
    assert message["gitLink"] == "https://link-to-be-patched"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 2.5


@pytest.mark.parametrize("template_uuid", ["uuid_3"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_201_created_by_user_1(response: Response) -> None:
    """Tests the response status code is 201 and valid."""
    # Assert response is valid
    assert response.status_code == 201
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "8fc20f81-e0a9-471c-8008-697ce799e73b"
    assert message["repoFile"] == "my_template_3.json"
    assert message["title"] == "My Template 3"
    assert message["summary"] == "Template example 3"
    assert message["language"] == "Python"
    assert sorted(message["tags"]) == ["Tag3"]
    assert message["picture"] == "https://picture-url/template"
    assert message["gitLink"] == "https://some-git-link/template"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 1.0


@pytest.mark.parametrize("template_uuid", ["uuid_4"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer new_user-token"}], indirect=True)
def test_201_created_by_new_user(response: Response) -> None:
    """Tests the response status code is 201 and valid."""
    # Assert response is valid
    assert response.status_code == 201
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "f3f35224-e35c-46a4-90d1-354646970b13"
    assert message["repoFile"] == "my_template_4.json"
    assert message["title"] == "My Template 4"
    assert message["summary"] == "Template example 4"
    assert message["language"] == "Python"
    assert sorted(message["tags"]) == []
    assert message["picture"] == "https://picture-url/template"
    assert message["gitLink"] == "https://some-git-link/template"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 3.0


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer bad-token"}, {}], indirect=True)
def test_401_unauthorized(response: Response) -> None:
    """Tests the response status code is 401 and valid."""
    # Assert response is valid
    assert response.status_code == 401
    # Assert header is valid
    assert response.headers["WWW-Authenticate"] == "Bearer"
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "authentication"
    assert message["detail"][0]["loc"] == ["header", "bearer"]
    assert "Not authenticated" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["unknown"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_404_not_found(response: Response) -> None:
    """Tests the response status code is 404 and valid."""
    # Assert response is valid
    assert response.status_code == 404
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "not_found"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Template not found" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["bad_uuid"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_422_bad_uuid(response: Response) -> None:
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["a"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_422_bad_score(response: Response) -> None:
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "json_invalid"
    assert message["detail"][0]["loc"] == ["body", 0]
    assert "JSON decode error" in message["detail"][0]["msg"]


@pytest.mark.usefixtures("patch_session_get_error")
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer user_1-token"}], indirect=True)
def test_500_server_error(response: Response) -> None:
    """Tests the response status code is 500 and valid."""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"
