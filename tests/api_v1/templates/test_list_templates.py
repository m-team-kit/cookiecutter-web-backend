"""Tests for the list templates endpoint."""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import pytest


@pytest.fixture(scope="module")
def response(client, patch_session, query, headers):
    """Performs a POST request to create a database."""
    response = client.get("/api/v1/templates/", params=query, headers=headers)
    return response


@pytest.mark.parametrize("query", [{}], indirect=True)
def test_200_ok_all(response):
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 4


@pytest.mark.parametrize("query", [{"sort_by": "-score"}, {}], indirect=True)
def test_200_score_desc(response):
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    templates = response.json()
    assert templates[0]["score"] == 5.0
    assert templates[1]["score"] == 4.5
    assert templates[2]["score"] is None
    assert templates[3]["score"] is None


@pytest.mark.parametrize("query", [{"sort_by": "+score"}, {"sort_by": "+score,+title"}], indirect=True)
def test_200_score_asc(response):
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    templates = response.json()
    assert templates[0]["score"] == 4.5
    assert templates[1]["score"] == 5.0
    assert templates[2]["score"] is None
    assert templates[3]["score"] is None


@pytest.mark.parametrize("query", [{"sort_by": "+title"}], indirect=True)
def test_200_title_asc(response):
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    templates = response.json()
    assert templates[0]["title"] == "My Template 1"
    assert templates[1]["title"] == "My Template 2"
    assert templates[2]["title"] == "My Template 3"
    assert templates[3]["title"] == "My Template 4"


@pytest.mark.parametrize("query", [{"language": "Python"}, {"language": "python"}], indirect=True)
def test_200_message(response):
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    templates = sorted(response.json(), key=lambda x: x["title"])
    assert len(templates) == 4
    assert templates[0]["title"] == "My Template 1"
    assert templates[1]["title"] == "My Template 2"
    assert templates[2]["title"] == "My Template 3"
    assert templates[3]["title"] == "My Template 4"


@pytest.mark.parametrize("query", [{"tags": ["Tag1", "Tag2"]}, {"tags": ["tag1", "tag2"]}], indirect=True)
def test_200_tags(response):
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    templates = sorted(response.json(), key=lambda x: x["title"])
    assert len(templates) == 1
    assert templates[0]["title"] == "My Template 1"


@pytest.mark.parametrize("query", [{"keywords": ["my", "example"]}], indirect=True)
def test_200_keywords(response):
    """Tests the response status code is 200 and valid."""
    assert response.status_code == 200
    templates = sorted(response.json(), key=lambda x: x["title"])
    assert len(templates) == 2
    assert templates[0]["title"] == "My Template 3"
    assert templates[1]["title"] == "My Template 4"


@pytest.mark.parametrize("query", [{"sort_by": "bad_sort"}], indirect=True)
def test_422_bad_sortby(response):
    """Tests the response status code is 422 and valid."""
    assert response.status_code == 422
    message = response.json()
    assert message["detail"][0]["type"] == "value_error"
    assert message["detail"][0]["loc"] == ["query", "sort_by"]
    assert "Value error, Invalid sort by option" in message["detail"][0]["msg"]


@pytest.mark.parametrize("patch_session", [Exception("error")], indirect=True)
def test_500_database_error(response):
    """Tests the response status code is 500 and valid."""
    assert response.status_code == 500
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"
