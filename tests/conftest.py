"""Defines fixtures available to all tests.
See: https://fastapi.tiangolo.com/tutorial/testing/
"""
# pylint: disable=redefined-outer-name
import os
import tomllib

import pytest
from flaat.user_infos import UserInfos
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor


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


@pytest.fixture(scope="session", autouse=True)
def sql_database(config, postgresql_proc):
    """Returns a state maintained database of postgresql"""
    config["DATABASE"]["host"] = postgresql_proc.host
    config["DATABASE"]["port"] = postgresql_proc.port
    config["DATABASE"]["user"] = postgresql_proc.user
    with DatabaseJanitor(**config["DATABASE"]) as database:
        yield database
