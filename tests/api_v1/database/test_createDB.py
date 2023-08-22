# pylint: disable=redefined-outer-name
from uuid import UUID
from typing import Dict, List
import pytest
from fastapi import Response
from fastapi.testclient import TestClient
from app.models.template import Template


@pytest.fixture(scope="module")
def response(client: TestClient, headers: Dict) -> None:
    """Performs a POST request to create a database."""
    response = client.post("/api/v1/db:create", headers=headers)
    return response


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_HTTP_204_NO_CONTENT(response: Response) -> None:
    """Tests the response status code is 204 and valid."""
    assert response.status_code == 204


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer bad-secret"}], indirect=True)
def test_HTTP_401_UNAUTHORIZED(response: Response) -> None:
    """Tests the response status code is 401 and valid."""
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect secret"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{}], indirect=True)
def test_HTTP_403_UNAUTHORIZED(response: Response) -> None:
    """Tests the response status code is 403 and valid."""
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_DB_templates(templates: List[Template]) -> None:
    """Tests the database contains the correct templates."""
    assert isinstance(templates[0].id, UUID)
    assert templates[0].repoFile == "my_template_1.json"
    assert templates[0].title == "My Template 1"
    assert templates[0].summary == "Template example 1"
    assert templates[0].language == "Python"
    assert templates[0].tags == ["Tag1", "Tag2"]
    assert templates[0].picture == "https://picture-url/template_1"
    assert templates[0].gitLink == "https://some-git-link/template_1"
    assert templates[0].gitCheckout == "main"


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_DB_scores(templates: List[Template]) -> None:
    """Tests the database contains the correct templates."""
    for template in templates:
        assert template.score == 0.0
        assert template.scores == ""
