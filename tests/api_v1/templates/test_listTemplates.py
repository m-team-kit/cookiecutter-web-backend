# pylint: disable=redefined-outer-name
from typing import Dict

import pytest
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def response(client: TestClient, query: Dict, headers: Dict) -> None:
    """Performs a POST request to create a database."""
    response = client.get("/api/v1/templates/", params=query, headers=headers)
    return response


@pytest.mark.parametrize("query", [{}], indirect=True)
def test_200_ok_all(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 4


@pytest.mark.parametrize("query", [{}], indirect=True)
def test_200_ok_order(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    # TODO: Add parametrization to select order
    # !!!!!!
    assert [x["score"] for x in response.json()] == [5.0, 4.5, None, None]


@pytest.mark.parametrize("query", [{"language": "Python"}], indirect=True)
def test_200_ok_message(response: Response, query: Dict) -> None:
    """Tests the response status code is 200 and valid."""
    templates = response.json()
    assert all(template["language"] == query["language"] for template in templates)


@pytest.mark.parametrize("query", [{"tags": ["Tag1", "Tag2"]}], indirect=True)
def test_200_ok_tags(response: Response, query: Dict) -> None:
    """Tests the response status code is 200 and valid."""
    templates = response.json()
    assert all(tag in template["tags"] for tag in query["tags"] for template in templates)


@pytest.mark.parametrize("query", [{"keywords": ["my", "example"]}], indirect=True)
def test_200_ok_keywords(response: Response, query: Dict) -> None:
    """Tests the response status code is 200 and valid."""
    templates, keys = response.json(), query["keywords"]
    assert all(k in t["title"] or k in t["summary"] for k in keys for t in templates)
