"""Tests for rate_template API endpoint."""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import pytest


@pytest.fixture(scope="module")
def response(client, patch_session, template_uuid, headers, body):
    """Performs a POST request to create a database."""
    response = client.put(f"/api/v1/templates/{template_uuid}/score", content=body, headers=headers)
    return response


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["1", "1.0"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_200_updated_by_user_1(response):
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "bced037a-a326-425d-aa03-5d3cbc9aa3d1"
    assert message["repoFile"] == "my_template_1.json"
    assert message["title"] == "My Template 1"
    assert message["summary"] == "Tests Cookiecutter"
    assert set(message["tags"]) == set(["rust", "python"])
    assert message["picture"] == "path/to/picture.png"
    assert message["gitLink"] == "https://link-to-be-patched"
    assert message["feedback"] == "https://link-to-feedback"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 1.0


@pytest.mark.parametrize("template_uuid", ["uuid_4"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_201_created_by_user_1(response):
    """Tests the response status code is 201 and valid."""
    # Assert response is valid
    assert response.status_code == 201
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "f3f35224-e35c-46a4-90d1-354646970b13"
    assert message["repoFile"] == "my_template_4.json"
    assert message["title"] == "My Template 4"
    assert message["summary"] == "Template example 4"
    assert message["tags"] == []
    assert message["picture"] == "path/to/picture.png"
    assert message["gitLink"] == "https://some-git-link/template"
    assert message["feedback"] == "https://link-to-feedback"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 1.0


@pytest.mark.parametrize("template_uuid", ["uuid_4"], indirect=True)
@pytest.mark.parametrize("body", ["1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["new_user-token"], indirect=True)
def test_201_created_by_new_user(response):
    """Tests the response status code is 201 and valid."""
    # Assert response is valid
    assert response.status_code == 201
    # Assert template in response is valid
    message = response.json()
    assert message["id"] == "f3f35224-e35c-46a4-90d1-354646970b13"
    assert message["repoFile"] == "my_template_4.json"
    assert message["title"] == "My Template 4"
    assert message["summary"] == "Template example 4"
    assert message["tags"] == []
    assert message["picture"] == "path/to/picture.png"
    assert message["gitLink"] == "https://some-git-link/template"
    assert message["feedback"] == "https://link-to-feedback"
    assert message["gitCheckout"] == "main"
    assert message["score"] == 1.0


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["1", "1.0"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["bad-token", None], indirect=True)
def test_401_unauthorized(response):
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
@pytest.mark.parametrize("body", ["1", "1.0"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
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
@pytest.mark.parametrize("body", ["1", "1.0"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_422_bad_uuid(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["-1", "-1.0"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_422_greater_than_equal(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "greater_than_equal"
    assert message["detail"][0]["loc"] == ["body"]
    assert "should be greater than or equal" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["6", "6.0"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_422_less_than_equal(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "less_than_equal"
    assert message["detail"][0]["loc"] == ["body"]
    assert "should be less than or equal" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["-0.1", "2.5", "5.1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_422_int_from_float(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "int_from_float"
    assert message["detail"][0]["loc"] == ["body"]
    assert "Input should be a valid integer" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["a", "."], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_422_bad_score(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "json_invalid"
    assert message["detail"][0]["loc"] == ["body", 0]
    assert "JSON decode error" in message["detail"][0]["msg"]


@pytest.mark.parametrize("patch_session", [Exception("error")], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", ["1", "1.0"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_500_database_error(response):
    """Tests the response status code is 500 and valid."""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"
