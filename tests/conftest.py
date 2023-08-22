"""Defines fixtures available to all tests.
See: https://fastapi.tiangolo.com/tutorial/testing/
"""
# pylint: disable=redefined-outer-name
import os
import tomllib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import create_app, crud
from app.core import database


@pytest.fixture(scope="session", params=["config-1"])
def configuration_path(request):
    """Fixture to provide each testing configuration path."""
    return f"tests/configurations/{request.param}.toml"


@pytest.fixture(scope="session", name="config")
def configuration(configuration_path):
    """Fixture to provide each testing configuration dict."""
    with open(configuration_path, mode="rb") as file:
        return tomllib.load(file)


@pytest.fixture(scope="session", autouse=True)
def environment(config, postgresql_proc):
    """Patch fixture to set test env variables."""
    os.environ["POSTGRES_SERVER"] = str(postgresql_proc.host)
    os.environ["POSTGRES_PORT"] = str(postgresql_proc.port)
    os.environ["POSTGRES_USER"] = str(postgresql_proc.user)
    os.environ["POSTGRES_PASSWORD"] = config["DATABASE"]["password"]
    os.environ["POSTGRES_DB"] = config["DATABASE"]["dbname"]
    for key, value in config["ENVIRONMENT"].items():
        os.environ[key] = value


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
    return create_engine(connection, echo=False, poolclass=NullPool)


@pytest.fixture(scope="session", autouse=True)
def create_all(sql_engine):
    """Create all tables in the database."""
    database.Base.metadata.create_all(bind=sql_engine)
    database.Token.metadata.create_all(bind=sql_engine)


@pytest.fixture(scope="module")
def session_generator(sql_engine):
    """Returns a database session generator of postgresql."""
    return sessionmaker(autocommit=False, autoflush=False, bind=sql_engine)


@pytest.fixture(scope="module", name="custom")
def custom_settings(request):
    """Fixture to provide each testing custom configuration values."""
    return request.param


@pytest.fixture(scope="module")
def app(custom):
    """Generate application from factories model."""
    return create_app(**custom)


@pytest.fixture(scope="module")
def client(app):
    """Produce test client from application instance."""
    return TestClient(app)


@pytest.fixture(scope="module")
def headers(request):
    """Fixture to provide each testing header."""
    return request.param if request.param else {}


@pytest.fixture(scope="module")
def templates(response, session_generator):
    """Fixture to provide database templates after request."""
    with session_generator() as session:
        templates = crud.template.get_multi(session, skip=0, limit=None)
        yield {Path(t.repoFile).stem: t for t in templates}
