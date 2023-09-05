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
- [ ] Add a `LICENSE` file
- [ ] Add a `CHANGELOG.md` file
- [ ] Add a `ISSUE_TEMPLATE.md` file
- [ ] Add a `PULL_REQUEST_TEMPLATE.md` file
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

This will run the application following the configuration in `compose.yml` and `production.yml` files.
It automatically loads the environment variables from the `.env` file and creates a postgres database.

If it is the first time you run the application or you have modified the models, you need to run the migrations.

```bash
$ docker compose -f docker-compose.yml -f compose/production.yml run --rm backend alembic upgrade head
```

For more details about the migrations, you can access [README](alembic/README.md) inside the `alembic` folder.

## Testing

There are multiple ways to run the tests. The standard way is to use `tox`:

```bash
$ tox
```

However, you can also run the tests with `pytest`:

```bash
$ pip install -r requirements.txt -r requirements-test.txt
$ python -m pytest tests
```

Or inside docker if you need to test the application in a clean environment:

```bash
$ docker-compose -f docker-compose.yml -f compose/testing.yml run --rm backend
```

## Development

If you need to run the application in local for debugging or development, you can use the following methods:

```bash
$ pip install -r requirements.txt -r requirements-dev.txt
```

This will run the application following the configuration in the `pyproject.toml` file. You can run your custom database or use the one in the `docker-compose.yml` file with the following command:

```bash
$ docker-compose -f docker-compose -f compose/development.yml up -d
```

Then you can run the application with the following command:

```bash
$ uvicorn autoapp:app --reload
```

Note that this does not load the environment variables from the `.env` file. You need to load them with your preferred method.
If you use vscode, you can run the application in debug mode using the `Python: FastAPI` configuration. This loads the `.env` file automatically.
