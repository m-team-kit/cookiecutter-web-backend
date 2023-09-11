# TODOs before releasing version 1.0.0

- [x] Add .vscode folder with launch, settings and dictionary files
  - [x] Add launch.json file to run the application in debug mode
  - [x] Add settings.json file to configure vscode
  - [x] Add dictionary file to configure vscode spell checker
- [x] Add alembic folder with first migration to build database
  - [x] Add alembic.ini file to configure alembic
  - [x] Configure env.py file to use alembic
  - [x] Add README file to explain how to use alembic
  - [x] Add first migration to build database
- [x] Implement factories model to run the application
  - [x] Configure **init**.py file to import create_app function
  - [x] Add autoapp.py file as start point to the application
- [x] Add app folder with all application requirements
  - [x] Add **init**.py file to import all required modules
  - [x] Add api_v1 folder with all required endpoints
    - [x] Add database endpoints
    - [x] Add project endpoints
    - [x] Add templates endpoints
    - [x] Add parameters for query, path and body
    - [x] Add schemas for requests and responses
  - [x] Add forward of api_latest endpoint to api_v1
  - [x] Add authentication functionalities for OIDC users
  - [x] Add authentication functionalities for admin secret key
  - [x] Add database functionalities and models with SQLAlchemy
  - [x] Add config file to load environment variables
  - [x] Add dependencies file to handle fastapi common handlers
  - [x] Add types file to implement custom types and validations
  - [x] Add utils file to implement common utilities
- [x] Add scripts folder to store application scripts
- [x] Add tests folder to test application endpoints
  - [x] Add api_v1 folder to test api_latest endpoints
  - [x] Add configurations folder to setup server
  - [x] Add repositories folder to test database functionalities
  - [x] Add generic conftest.py file with common fixtures
  - [x] Add setup_db.sql script to set database values for tests
- [x] Add .env.sample file as template for environment variables
- [x] Add .gitignore file to ignore files and folders
- [x] Add docker-compose.yml file to run the application as container
- [x] Add favicon.ico file to display favicon in browser
- [x] Add pyproject.toml
- [x] Migrate from poetry to normal pip
- [x] Add a `README.md` file
- [x] Add tox.ini file to run tests in multiple environments
  - [x] Add py311 environment to run tests in python 3.11
  - [x] Add qc.cov environment to run coverage tests
  - [x] Add qc.sec environment to run security tests
  - [x] Add qc.sty environment to run style tests
  - [x] Fix requirement of psycopg_binary for testing

# Cookiecutter Web Backend

Implemented using:

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Installation and run

There standard way to run the application is via docker-compose:

```bash
$ docker compose -f docker-compose.yml -f compose/production.yml up -d
```

See [Use Compose in production](https://docs.docker.com/compose/production/) for more information.

This will run the application following the configuration in `compose.yml` and `production.yml` files. It automatically loads the environment variables from the `.env` file and creates a postgres database.

## Testing

Tests are implemented using [pytest](https://docs.pytest.org/en/latest/). The tests are designed to run on the integration layer, therefore they require a database and an smtp server running.

There are multiple ways to run the tests. The standard way is to use `docker compose`:

```bash
$ docker compose -f docker-compose.yml -f compose/testing.yml up --rm --exit-code-from backend
```

This will run the tests inside a container with all the required dependencies and services.

> Testing does not read the `.env` file. You need to edit `compose/testing.yml` to set the environment variables.

## Development

There are multiple ways and tools that can be used to develop the application. The standard way is to use `docker compose`:

```bash
$ docker compose -f docker-compose.yml -f compose/development.yml up -d
```

Then you can attach your debugger to the running container.

```bash

```

For vscode the `launch.json` contains a configuration `Python: Attach backend` to attach the debugger to the running backend.

The `backend` service is configured to do not start until a debugger is attached. Therefore you do not need to use the container to debug your application. You can also use locally `uvicorn`:

```bash
$ pip install -r requirements.txt -r requirements-dev.txt
$ uvicorn autoapp:app --reload
```

> Note that this does not load the environment variables from the `.env` file. You need to load them with your preferred method.

For vscode the `launch.json` contains a configuration `Python: FastAPI` to directly lunch the application in local.

## Coverage and other tools

You can get extended testing features by running tox:

```bash
$ tox
```

You have the following environments configured:

- `py311`: run tests in python 3.11
- `qc.cov`: run coverage tests
- `qc.sec`: run security tests
- `qc.sty`: run style tests
