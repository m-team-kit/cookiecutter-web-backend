from uuid import UUID

import pytest

template_options = {
    "uuid_1": "bced037a-a326-425d-aa03-5d3cbc9aa3d1",
    "uuid_2": "ef231acb-0ff9-4391-ab18-6cb2698b0985",
    "uuid_3": "8fc20f81-e0a9-471c-8008-697ce799e73b",
    "uuid_4": "f3f35224-e35c-46a4-90d1-354646970b13",
    "unknown": "00000000-0000-0000-0000-000000000000",
    "bad_uuid": "bad_uuid",
}


@pytest.fixture(scope="module")
def template_uuid(request) -> UUID:
    """Returns template UUID from setup_db.sql."""
    return template_options[request.param]


@pytest.fixture(scope="module")
def response_json(response):
    """Returns response json."""
    return response.json()
