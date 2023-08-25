# pylint: disable=unused-argument
from unittest.mock import Mock, patch
from uuid import UUID

import flaat
import pytest
from flaat.exceptions import FlaatUnauthenticated

template_options = {
    "uuid_1": "bced037a-a326-425d-aa03-5d3cbc9aa3d1",
    "uuid_2": "ef231acb-0ff9-4391-ab18-6cb2698b0985",
    "uuid_3": "8fc20f81-e0a9-471c-8008-697ce799e73b",
    "uuid_4": "f3f35224-e35c-46a4-90d1-354646970b13",
    "unknown": "00000000-0000-0000-0000-000000000000",
    "bad_uuid": "bad_uuid",
}

user_options = {
    "user_1-token": ("user_1", "issuer_1"),
    "user_2-token": ("user_2", "issuer_1"),
    "new_user-token": ("user_3", "issuer_2"),
}


@pytest.fixture(scope="module")
def template_uuid(request) -> UUID:
    """Returns template UUID from setup_db.sql."""
    return template_options[request.param]


@pytest.fixture(scope="module")
def response_json(response):
    """Returns response json."""
    return response.json()


@pytest.fixture(scope="module", autouse=True)
def patch_flaat():
    """Patch fixture to set test env variables."""
    with patch.object(flaat.BaseFlaat, "get_user_infos_from_access_token", side_effect=user_patch):
        yield


def user_patch(access_token: str, issuer_hint: str = ""):
    """Patch fixture that returns mocked token information."""
    try:
        token_info = Mock()
        token_info.subject = user_options[access_token][0]
        token_info.issuer = user_options[access_token][1]
        return token_info
    except KeyError:
        raise FlaatUnauthenticated() from None
