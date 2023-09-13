"""Tests for the update_db endpoint."""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import UUID

import pytest


@pytest.fixture(scope="module")
def response(client, patch_session, patch_repository, headers):
    """Performs a POST request to update a database."""
    response = client.post("/api/v1/db:update", headers=headers)
    return response


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_no_content(response, templates):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert database contains the correct templates
    assert len(templates) == 4
    assert "my_template_3" not in templates
    assert "my_template_5" in templates
    # Assert templates are correct
    assert isinstance(templates["my_template_1"].id, UUID)
    assert templates["my_template_1"].repoFile == "my_template_1.json"
    assert templates["my_template_1"].title == "Edited Template 1"
    assert templates["my_template_1"].summary == "Template edited 1"
    assert templates["my_template_1"].language == "python"
    assert templates["my_template_1"].tags == set(["tag1", "tag9"])
    assert templates["my_template_1"].picture == "https://picture-url/template_1"
    assert templates["my_template_1"].gitLink == "https://some-git-link/template_1"
    assert templates["my_template_1"].gitCheckout == "dev"
    # Assert scores are correct
    assert templates["my_template_1"].score == 4.5
    assert templates["my_template_2"].score is None
    assert templates["my_template_4"].score == 5.0
    assert templates["my_template_5"].score is None


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", [None], indirect=True)
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


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["bad-secret"], indirect=True)
def test_403_forbidden(response):
    """Tests the response status code is 403 and valid."""
    # Asset response is valid
    assert response.status_code == 403
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "authentication"
    assert message["detail"][0]["loc"] == ["header", "bearer"]
    assert "Incorrect secret" in message["detail"][0]["msg"]


@pytest.mark.parametrize("patch_repository", ["repository_down"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_500_repository_down(response):
    """Tests the response status code is 500 and valid.""" ""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"


@pytest.mark.parametrize("patch_session", [Exception("error")], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_500_database_error(response):
    """Tests the response status code is 500 and valid."""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"
