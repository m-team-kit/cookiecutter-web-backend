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


@pytest.mark.parametrize("query", [{"sort_by": "-score"}, {}], indirect=True)
def test_200_score_desc(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    templates = response.json()
    assert templates[0]["score"] == 5.0
    assert templates[1]["score"] == 4.5
    assert templates[2]["score"] is None
    assert templates[3]["score"] is None


@pytest.mark.parametrize("query", [{"sort_by": "+score"}, {"sort_by": "+score,+title"}], indirect=True)
def test_200_score_asc(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    templates = response.json()
    assert templates[0]["score"] == 4.5
    assert templates[1]["score"] == 5.0
    assert templates[2]["score"] is None
    assert templates[3]["score"] is None


@pytest.mark.parametrize("query", [{"sort_by": "+title"}], indirect=True)
def test_200_title_asc(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    templates = response.json()
    assert templates[0]["title"] == "My Template 1"
    assert templates[1]["title"] == "My Template 2"
    assert templates[2]["title"] == "My Template 3"
    assert templates[3]["title"] == "My Template 4"


@pytest.mark.parametrize("query", [{"language": "Python"}], indirect=True)
def test_200_message(response: Response, query: Dict) -> None:
    """Tests the response status code is 200 and valid."""
    templates = response.json()
    assert all(template["language"] == query["language"] for template in templates)


@pytest.mark.parametrize("query", [{"tags": ["Tag1", "Tag2"]}], indirect=True)
def test_200_tags(response: Response, query: Dict) -> None:
    """Tests the response status code is 200 and valid."""
    templates = response.json()
    assert all(tag in template["tags"] for tag in query["tags"] for template in templates)


@pytest.mark.parametrize("query", [{"keywords": ["my", "example"]}], indirect=True)
def test_200_keywords(response: Response, query: Dict) -> None:
    """Tests the response status code is 200 and valid."""
    templates, keys = response.json(), query["keywords"]
    assert all(k in t["title"] or k in t["summary"] for k in keys for t in templates)


@pytest.mark.parametrize("query", [{"sort_by": "bad_sort"}], indirect=True)
def test_422_bad_sortby(response: Response) -> None:
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "value_error"
    assert message["detail"][0]["loc"] == ["query", "sort_by"]
    assert "Value error, Invalid sort by option" in message["detail"][0]["msg"]


@pytest.mark.usefixtures("patch_session_get_error")
def test_500_server_error(response: Response) -> None:
    """Tests the response status code is 500 and valid."""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == []
    assert message["detail"][0]["msg"] == "Internal Server Error"
