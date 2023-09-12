"""Defines fixtures available to all tests.
See: https://fastapi.tiangolo.com/tutorial/testing/
"""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import os
import tomllib
from unittest.mock import Mock, patch

import flaat
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import orm
from starlette.routing import Mount

from app import create_app, database

# Configuration fixtures ------------------------------------------------------
# -----------------------------------------------------------------------------


@pytest.fixture(scope="session")
def configuration_path(request):
    """Fixture to provide each testing configuration path."""
    config_stem = request.param if hasattr(request, "param") else "standard-configuration"
    return f"tests/configurations/{config_stem}.toml"


@pytest.fixture(scope="session", name="config")
def configuration(configuration_path):
    """Fixture to provide each testing configuration dict."""
    with open(configuration_path, mode="rb") as file:
        return tomllib.load(file)


@pytest.fixture(scope="session", autouse=True)
def environment(config):
    """Patch fixture to set test env variables if not defined."""
    for key, value in config["ENVIRONMENT"].items():
        if key not in os.environ:
            os.environ[key] = value


# Database fixtures -----------------------------------------------------------
# -----------------------------------------------------------------------------


@pytest.fixture(scope="module")
def sql_session(client):
    """Returns the database session used in the test client methods."""
    # pylint: disable=invalid-name
    SessionLocal = orm.sessionmaker(client.app.state.sql_engine, autoflush=False, autocommit=False)
    with SessionLocal() as session:
        session.commit = session.flush  # Make sure to flush instead of commit
        yield session


@pytest.fixture(scope="module", autouse=True)
def patch_session(request, client, sql_session):
    """Patch database.get_session with mock returning sql_session."""
    if hasattr(request, "param") and isinstance(request.param, Exception):
        mock = Mock(orm.Session, side_effect=request.param)
        mock.query.side_effect = request.param
        mock.flush.side_effect = request.param
    else:
        mock = sql_session
    for mount in client.app.routes:
        if isinstance(mount, Mount):
            mount.app.dependency_overrides[database.get_session] = lambda: mock


# Request parametrization fixtures --------------------------------------------
# -----------------------------------------------------------------------------


@pytest.fixture(scope="module")
def client(request):
    """Generate application from factories model."""
    custom_parameters = request.param if hasattr(request, "param") else {}
    app = create_app(**custom_parameters)
    return TestClient(app)


@pytest.fixture(scope="module", name="query")
def query_parameters(request):
    """Fixture to provide each testing query parameters."""
    return request.param if hasattr(request, "param") else None


@pytest.fixture(scope="module", name="headers")
def header_parameters(authorization_bearer):
    """Fixture to provide each testing header."""
    headers = {}  # Create empty headers to fill with fixtures
    if authorization_bearer:
        headers["Authorization"] = f"Bearer {authorization_bearer}"
    return headers if headers else None


@pytest.fixture(scope="module", name="body")
def body_parameters(request):
    """Fixture to provide each testing body."""
    return request.param if hasattr(request, "param") else None


# Fixture options for template uuid -------------------------------------------
# -----------------------------------------------------------------------------
template_options = {
    "uuid_1": "bced037a-a326-425d-aa03-5d3cbc9aa3d1",
    "uuid_2": "ef231acb-0ff9-4391-ab18-6cb2698b0985",
    "uuid_3": "8fc20f81-e0a9-471c-8008-697ce799e73b",
    "uuid_4": "f3f35224-e35c-46a4-90d1-354646970b13",
    "unknown": "00000000-0000-0000-0000-000000000000",
    "bad_uuid": "bad_uuid",
}


@pytest.fixture(scope="module")
def template_uuid(request):
    """Returns template UUID from setup_db.sql."""
    return template_options[request.param]


# Fixture options for users ---------------------------------------------------
# -----------------------------------------------------------------------------
authentication_options = {
    "user_1-token": {"subject": "user_1", "issuer": "issuer_1"},
    "user_2-token": {"subject": "user_2", "issuer": "issuer_1"},
    "new_user-token": {"subject": "user_3", "issuer": "issuer_2"},
}


@pytest.fixture(scope="module")
def authorization_bearer(request):
    """Patches the token information for the user."""
    if hasattr(request, "param") and request.param in authentication_options:
        get_info = lambda _: Mock(**authentication_options[request.param])
        with patch.object(flaat.BaseFlaat, "get_user_infos_from_access_token", side_effect=get_info):
            yield request.param
    else:
        yield request.param if hasattr(request, "param") else None
