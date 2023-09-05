# pylint: disable=missing-module-docstring,redefined-outer-name
from typing import Dict

import pytest
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def response(client: TestClient, template_uuid: str, headers: Dict) -> None:
    """Performs a POST request to create a database."""
    response = client.get(f"/api/v1/project/{template_uuid}", headers=headers)
    return response


@pytest.mark.usefixtures("patch_fields_url")
@pytest.mark.parametrize("patch_fields_url", ["cookiecutter_1"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_200_length(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    # Assert response is valid
    assert response.status_code == 200
    # Assert template in response is valid
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5


@pytest.mark.usefixtures("patch_fields_url")
@pytest.mark.parametrize("patch_fields_url", ["cookiecutter_1"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_200_text_field(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    field = response.json()[0]
    assert field["type"] == "text"
    assert field["name"] == "text_field"
    assert field["prompt"] == "Text field example:"
    assert field["default"] == "My text field"


@pytest.mark.usefixtures("patch_fields_url")
@pytest.mark.parametrize("patch_fields_url", ["cookiecutter_1"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_200_composed_field(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    field = response.json()[1]
    assert field["type"] == "text"
    assert field["name"] == "composed_var"
    assert field["prompt"] == "Composed variable example:"
    assert field["default"] == "{{ cookiecutter.text_field|lower|replace(' ', '_') }}"


@pytest.mark.usefixtures("patch_fields_url")
@pytest.mark.parametrize("patch_fields_url", ["cookiecutter_1"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_200_checkbox_field(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    field = response.json()[2]
    assert field["type"] == "checkbox"
    assert field["name"] == "checkbox_field"
    assert field["prompt"] == "Checkbox field example:"
    assert field["default"] is True


@pytest.mark.usefixtures("patch_fields_url")
@pytest.mark.parametrize("patch_fields_url", ["cookiecutter_1"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_1"], indirect=True)
def test_200_select_field(response: Response) -> None:
    """Tests the response status code is 200 and valid."""
    field = response.json()[3]
    assert field["type"] == "select"
    assert field["name"] == "select_field"
    assert field["options"][0] == {"name": "option_1", "prompt": "Option 1 example"}
    assert field["options"][1] == {"name": "option_2", "prompt": "Option 2 example"}
    assert field["options"][2] == {"name": "option_3", "prompt": None}
    assert field["prompt"] == "Select field example:"
    assert field["default"] == "option_1"


@pytest.mark.parametrize("template_uuid", ["unknown"], indirect=True)
def test_404_not_found(response: Response) -> None:
    """Tests the response status code is 404 and valid."""
    # Assert response is valid
    assert response.status_code == 404
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "not_found"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Template not found" in message["detail"][0]["msg"]


@pytest.mark.parametrize("template_uuid", ["bad_uuid"], indirect=True)
def test_422_validation_error(response: Response) -> None:
    """Tests the response status code is 422 and valid."""
    # Assert response is valid
    assert response.status_code == 422
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "uuid_parsing"
    assert message["detail"][0]["loc"] == ["path", "uuid"]
    assert "Input should be a valid UUID" in message["detail"][0]["msg"]


@pytest.mark.usefixtures("patch_fields_url")
@pytest.mark.parametrize("patch_fields_url", ["repository_down"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_2"], indirect=True)
def test_500_server_error(response: Response) -> None:
    """Tests the response status code is 500 and valid.""" ""
    # Assert response is valid
    assert response.status_code == 500
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "server_error"
    assert message["detail"][0]["loc"] == ["server"]
    assert message["detail"][0]["msg"] == "Internal Server Error"


@pytest.mark.usefixtures("patch_fields_url")
@pytest.mark.parametrize("patch_fields_url", ["cookiecutter_2"], indirect=True)
@pytest.mark.parametrize("template_uuid", ["uuid_3"], indirect=True)
def test_501_not_implemented(response: Response) -> None:
    """Tests the response status code is 501 and valid.""" ""
    # Assert response is valid
    assert response.status_code == 501
    # Assert message is valid
    message = response.json()
    assert message["detail"][0]["type"] == "not_implemented"
    assert message["detail"][0]["loc"] == ["gitLink", "gitCheckout", "cookiecutter.json"]
    assert f"Field type '{dict}' not supported." in message["detail"][0]["msg"]
