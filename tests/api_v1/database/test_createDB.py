# pylint: disable=redefined-outer-name
from typing import Dict, List
from uuid import UUID

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from app.models.template import Template


@pytest.fixture(scope="module")
def response(client: TestClient, headers: Dict) -> None:
    """Performs a POST request to create a database."""
    response = client.post("/api/v1/db:create", headers=headers)
    return response


@pytest.mark.parametrize("headers", [{"authorization": "bearer 6de44315b565ea73f778282d"}], indirect=True)
def test_204_no_content(response: Response, templates: List[Template]) -> None:
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
    assert templates["my_template_1"].language == "Python"
    assert templates["my_template_1"].tags == set(["Tag1", "Tag2"])
    assert templates["my_template_1"].picture == "https://picture-url/template_1"
    assert templates["my_template_1"].gitLink == "https://some-git-link/template_1"
    assert templates["my_template_1"].gitCheckout == "dev"
    # Assert scores are correct
    assert templates["my_template_1"].score is None
    assert templates["my_template_2"].score is None
    assert templates["my_template_4"].score is None
    assert templates["my_template_5"].score is None


@pytest.mark.parametrize("headers", [{"authorization": "bearer bad-secret"}], indirect=True)
def test_401_unauthorized(response: Response) -> None:
    """Tests the response status code is 401 and valid."""
    # Assert response is valid
    assert response.status_code == 401
    # Assert header is valid
    assert response.headers["WWW-Authenticate"] == "Bearer"
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Incorrect secret"}


@pytest.mark.parametrize("headers", [{}], indirect=True)
def test_403_forbidden(response: Response) -> None:
    """Tests the response status code is 403 and valid."""
    # Asset response is valid
    assert response.status_code == 403
    # Assert message is valid
    message = response.json()
    assert message == {"detail": "Not authenticated"}
