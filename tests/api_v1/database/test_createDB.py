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
def test_204_no_content(response: Response) -> None:
    """Tests the response status code is 204 and valid."""
    assert response.status_code == 204


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer bad-secret"}], indirect=True)
def test_401_unauthorized(response: Response) -> None:
    """Tests the response status code is 401 and valid."""
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect secret"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{}], indirect=True)
def test_403_forbidden(response: Response) -> None:
    """Tests the response status code is 403 and valid."""
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_DB_length(templates: List[Template]) -> None:
    assert len(templates) == 3


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_DB_template(templates: List[Template]) -> None:
    """Tests the database contains the correct templates."""
    assert isinstance(templates["my_template_1"].id, UUID)
    assert templates["my_template_1"].repoFile == "my_template_1.json"
    assert templates["my_template_1"].title == "My Template 1"
    assert templates["my_template_1"].summary == "Template example 1"
    assert templates["my_template_1"].language == "Python"
    assert sorted(x.name for x in templates["my_template_1"].tags) == ["Tag1", "Tag2"]
    assert templates["my_template_1"].picture == "https://picture-url/template_1"
    assert templates["my_template_1"].gitLink == "https://some-git-link/template_1"
    assert templates["my_template_1"].gitCheckout == "main"


@pytest.mark.parametrize("custom", [{"secret": "6de44315b565ea73f778282d"}], indirect=True)
@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_DB_scores(templates: List[Template]) -> None:
    """Tests the database contains the correct templates."""
    for template in templates.values():
        assert template.score == None
        assert template.scores == []
