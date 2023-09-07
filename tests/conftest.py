"""Defines fixtures available to all tests.
See: https://fastapi.tiangolo.com/tutorial/testing/
"""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import os
import tomllib
from mailbox import Maildir
from operator import itemgetter
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
from uuid import UUID

import flaat
import pytest
import sqlalchemy as sa
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Mailbox
from fastapi.testclient import TestClient
from flaat.exceptions import FlaatUnauthenticated
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import create_app, database, models


@pytest.fixture(scope="session", params=["config-1"])
def configuration_path(request):
    """Fixture to provide each testing configuration path."""
    return f"tests/configurations/{request.param}.toml"


@pytest.fixture(scope="session", name="config")
def configuration(configuration_path):
    """Fixture to provide each testing configuration dict."""
    with open(configuration_path, mode="rb") as file:
        return tomllib.load(file)


@pytest.fixture(scope="session")
def sql_database(config, postgresql_proc):
    """Returns a state maintained database of postgresql."""
    config["DATABASE"]["host"] = postgresql_proc.host
    config["DATABASE"]["port"] = postgresql_proc.port
    config["DATABASE"]["user"] = postgresql_proc.user
    with DatabaseJanitor(**config["DATABASE"]) as database:
        yield database


@pytest.fixture(scope="session")
def sql_engine(sql_database):
    """Returns a database engine of postgresql."""
    authentication = f"{sql_database.user}:{sql_database.password}"
    netloc = f"{sql_database.host}:{sql_database.port}"
    connection = f"postgresql+psycopg2://{authentication}@{netloc}/{sql_database.dbname}"
    return sa.create_engine(connection, echo=False, poolclass=NullPool)


@pytest.fixture(scope="session", autouse=True)
def environment(config, postgresql_proc):
    """Patch fixture to set test env variables."""
    os.environ["POSTGRES_HOST"] = str(postgresql_proc.host)
    os.environ["POSTGRES_PORT"] = str(postgresql_proc.port)
    os.environ["POSTGRES_USER"] = str(postgresql_proc.user)
    os.environ["POSTGRES_PASSWORD"] = config["DATABASE"]["password"]
    os.environ["POSTGRES_DB"] = config["DATABASE"]["dbname"]
    for key, value in config["ENVIRONMENT"].items():
        os.environ[key] = value


@pytest.fixture(scope="module", autouse=True)
def create_all(sql_engine):
    """Create all tables in the database."""
    database.Base.metadata.create_all(bind=sql_engine)
    with sql_engine.connect() as connection:
        with open("tests/setup_db.sql", encoding="utf-8") as file:
            query = sa.text(file.read())
        connection.execute(query)
        connection.commit()
    yield
    database.Base.metadata.drop_all(bind=sql_engine)


@pytest.fixture(scope="module")
def session_generator(sql_engine):
    """Returns a database session generator of postgresql."""
    return sessionmaker(autocommit=False, autoflush=False, bind=sql_engine)


@pytest.fixture(scope="module", name="mailbox", autouse=True)
def smtp_server(config):
    """Fixture to provide each testing SMTP server."""
    with TemporaryDirectory() as tempdir:
        maildir_path = os.path.join(tempdir, "maildir")
        controller = Controller(Mailbox(maildir_path), **config["SMTP"])
        controller.start()
        yield Maildir(maildir_path, create=False)
        controller.stop()


@pytest.fixture(scope="module", name="custom")
def custom_settings(request):
    """Fixture to provide each testing custom configuration values."""
    return request.param if hasattr(request, "param") else {}


@pytest.fixture(scope="module")
def app(custom):
    """Generate application from factories model."""
    return create_app(**custom)


@pytest.fixture(scope="module")
def client(app):
    """Produce test client from application instance."""
    return TestClient(app)


@pytest.fixture(scope="module", name="query")
def query_parameters(request):
    """Fixture to provide each testing query parameters."""
    return request.param if hasattr(request, "param") else {}


@pytest.fixture(scope="module", name="headers")
def header_parameters(request):
    """Fixture to provide each testing header."""
    return request.param if hasattr(request, "param") else {}


@pytest.fixture(scope="module", name="body")
def body_parameters(request):
    """Fixture to provide each testing body."""
    return request.param if hasattr(request, "param") else {}


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
def templates(response, session_generator):
    """Fixture to provide database templates after request."""
    with session_generator() as session:
        templates = session.query(models.Template).all()
        yield {Path(t.repoFile).stem: t for t in templates}


@pytest.fixture(scope="module")
def notifications(response, mailbox):
    """Fixture to provide email notifications after request."""
    return sorted(mailbox, key=itemgetter("subject"))


@pytest.fixture(scope="module", autouse=True)
def patch_flaat():
    """Patch fixture to set test env variables."""
    with patch.object(flaat.BaseFlaat, "get_user_infos_from_access_token", side_effect=user_patch):
        yield


user_options = {
    "user_1-token": Mock(subject="user_1", issuer="issuer_1"),
    "user_2-token": Mock(subject="user_2", issuer="issuer_1"),
    "new_user-token": Mock(subject="user_3", issuer="issuer_2"),
    "bad-token": None,
}


def user_patch(access_token: str, issuer_hint: str = ""):
    """Patch fixture that returns mocked token information."""
    try:
        return user_options[access_token]
    except KeyError:
        raise FlaatUnauthenticated() from None
