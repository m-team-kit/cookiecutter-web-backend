"""Tests for GET /api/v1/templates/{uuid} endpoint."""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import pytest


@pytest.fixture(scope="module")
def response(client, patch_session, template_uuid, headers):
    """Performs a POST request to create a database."""
    response = client.get(f"/api/v1/templates/{template_uuid}", headers=headers)
    return response


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_200_ok(response):
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "bced037a-a326-425d-aa03-5d3cbc9aa3d1"
    assert message["repoFile"] == "my_template_1.json"
    assert message["title"] == "My Template 1"
    assert message["summary"] == "Tests Cookiecutter"
    assert sorted(message["tags"]) == ["python", "rust"]
    assert message["picture"] == "https://link-to-be-patched/raw/main/path/to/picture.png"
    assert message["gitLink"] == "https://link-to-be-patched"
    assert message["gitCheckout"] == "main"


@pytest.mark.parametrize("template_uuid", ["unknown"], indirect=True)
def test_404_not_found(response):
    """Tests the response status code is 404 and valid."""
    # Assert response is valid
    assert response.status_code == 404
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "not_found"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Template not found" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["bad_uuid"], indirect=True)
def test_422_validation_error(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]
    assert message["detail"][0]["input"] == "bad_uuid"


@pytest.mark.parametrize("patch_session", [Exception("error")], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_500_database_error(response):
    """Tests the response status code is 500 and valid."""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"
