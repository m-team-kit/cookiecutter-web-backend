"""Tests for the generate project API endpoint.""" ""
# pylint: disable=redefined-outer-name
import io
import tomllib
import zipfile
from unittest.mock import Mock

import pytest


@pytest.fixture(scope="module")
def response(client, template_uuid, headers, body):
    """Performs a POST request to create a database."""
    response = client.post(f"/api/v1/project/{template_uuid}:generate", json=body, headers=headers)
    return response


@pytest.mark.parametrize("patch_cookiecutter", ["cookiecutter_1"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [{"text_field": "Some text"}], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_200_ok(response, body):
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert header is valid
    assert response.headers["content-type"] == "application/zip"
    # Assert template in response is valid
    sub_folder = f"{body['text_field'].lower().replace(' ', '_')}_project"
    zip_buffer = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, "r", zipfile.ZIP_DEFLATED, False) as archive:
        with archive.open(f"{sub_folder}/template_file.toml") as file:
            config = tomllib.load(file)
    assert config["text_field"] == body["text_field"]
    assert config["composed_var"] == body["text_field"].lower().replace(" ", "_")
    assert config["checkbox_field"] == "True"
    assert config["select_field"] == "option_1"
    assert config["no_prompt_var"] == "Some text"
    assert config["private_var"] == "This variable will not be rendered"


@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [{"text_field": "Some text"}], indirect=True)
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
@pytest.mark.parametrize("body", [{"text_field": "Some text"}], indirect=True)
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
@pytest.mark.parametrize("body", [{"text_field": "Some text"}], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_422_unprocessable_uuid(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["bad_uuid"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_422_no_body(response):
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]


@pytest.mark.parametrize("patch_cookiecutter", ["repository_down"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [{"text_field": "Some text"}], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["user_1-token"], indirect=True)
def test_500_repository_down(response):
    """Tests the response status code is 500 and valid.""" ""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"


@pytest.mark.parametrize("patch_session", [Mock(side_effect=Exception("error"))], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
@pytest.mark.parametrize("body", [{"text_field": "Some text"}], indirect=True)
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
