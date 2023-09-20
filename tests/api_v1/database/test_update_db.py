"""Tests for the update_db endpoint."""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import UUID

import pytest

from app import models


@pytest.fixture(scope="module")
def response(client, patch_session, patch_repository, headers):
    """Performs a POST request to update a database."""
    response = client.post("/api/v1/db:update", headers=headers)
    return response


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_correct_content(response, sql_session):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert database contains the correct templates
    templates = sorted(sql_session.query(models.Template).all(), key=lambda x: x.repoFile)
    assert len(templates) == 4
    assert all(isinstance(template.id, UUID) for template in templates)


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_correct_repo_file(response, sql_session):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert database contains the correct templates
    templates = sorted(sql_session.query(models.Template).all(), key=lambda x: x.repoFile)
    assert templates[0].repoFile == "my_template_1.json"
    assert templates[1].repoFile == "my_template_2.json"
    assert templates[2].repoFile == "my_template_4.json"
    assert templates[3].repoFile == "my_template_5.json"


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_correct_title(response, sql_session):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert database contains the correct templates
    templates = sorted(sql_session.query(models.Template).all(), key=lambda x: x.repoFile)
    assert templates[0].title == "Edited Template 1"
    assert templates[1].title == "Edited Template 2"
    assert templates[2].title == "Edited Template 4"
    assert templates[3].title == "My Template 5"


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_correct_picture(response, sql_session):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert database contains the correct templates
    templates = sorted(sql_session.query(models.Template).all(), key=lambda x: x.repoFile)
    assert templates[0].picture == "edited/picture.png"
    assert templates[1].picture == "edited/picture.png"
    assert templates[2].picture == "edited/picture.png"
    assert templates[3].picture == "edited/picture.png"


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_correct_scores(response, sql_session):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert scores are correct
    templates = sorted(sql_session.query(models.Template).all(), key=lambda x: x.repoFile)
    assert templates[0].score == 5.0
    assert templates[1].score is None
    assert templates[2].score is None
    assert templates[3].score is None
    scores = sql_session.query(models.Score).all()
    assert len(scores) == 1


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_correct_tags(response, sql_session):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert tags are correct
    templates = sorted(sql_session.query(models.Template).all(), key=lambda x: x.repoFile)
    assert templates[0].tags == set(["python", "postgres"])
    assert templates[1].tags == set(["python", "erlang"])
    assert templates[2].tags == set([])
    assert templates[3].tags == set(["python"])
    tags = sql_session.query(models.Tag).all()
    assert len(tags) == 3


@pytest.mark.parametrize("patch_repository", ["repository_1"], indirect=True)
@pytest.mark.parametrize("authorization_bearer", ["6de44315b565ea73f778282d"], indirect=True)
def test_204_correct_users(response, sql_session):
    """Tests the response status code is 204 and valid."""
    # Assert response is valid
    assert response.status_code == 204
    # Assert tags are correct
    users = sorted(sql_session.query(models.User).all(), key=lambda x: (x.issuer, x.subject))
    assert (users[0].subject, users[0].issuer) == ("user_1", "issuer_1")
    assert len(users) == 1


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
