# TODOs before releasing version 1.0.0

- [ ] Add .vscode folder with launch, settings and dictionary files
  - [x] Add launch.json file to run the application in debug mode
  - [x] Add settings.json file to configure vscode
  - [ ] Add dictionary file to configure vscode spell checker
- [ ] Add alembic folder with first migration to build database
  - [x] Add alembic.ini file to configure alembic
  - [x] Configure env.py file to use alembic
  - [ ] Add README file to explain how to use alembic
  - [ ] Add first migration to build database
- [ ] Implement factories model to run the application
  - [x] Configure **init**.py file to import create_app function
  - [x] Add autoapp.py file as start point to the application
- [ ] Add app folder with all application requirements
  - [x] Add **init**.py file to import all required modules
  - [x] Add api_v1 folder with all required endpoints
    - [x] Add database endpoints
    - [x] Add project endpoints
    - [x] Add templates endpoints
    - [x] Add parameters for query, path and body
    - [x] Add schemas for requests and responses
  - [ ] Add forward of api_latest endpoint to api_v1
  - [x] Add authentication functionalities for OIDC users
  - [x] Add authentication functionalities for admin secret key
  - [x] Add database functionalities and models with SQLAlchemy
  - [ ] Add email processing functionalities with basic templates
  - [x] Add config file to load environment variables
  - [x] Add dependencies file to handle fastapi common handlers
  - [x] Add types file to implement custom types and validations
  - [x] Add utils file to implement common utilities
- [ ] Add scripts folder to store application scripts
  - [ ] Add load_environment.sh file to load environment variables
- [ ] Add tests folder to test application endpoints
  - [ ] Add api_latest folder to test api_latest endpoints
  - [x] Add api_v1 folder to test api_latest endpoints
  - [x] Add configurations folder to setup server
  - [x] Add repositories folder to test database functionalities
  - [x] Add generic conftest.py file with common fixtures
  - [x] Add setup_db.sql script to set database values for tests
- [x] Add .env.sample file as template for environment variables
- [x] Add .gitignore file to ignore files and folders
- [x] Add docker-compose.yml file to run the application as container
- [x] Add favicon.ico file to display favicon in browser
- [x] Add pyproject.toml file to manage dependencies with poetry
- [ ] Add a `README.md` file
- [ ] Add a `LICENSE` file
- [ ] Add a `CHANGELOG.md` file
- [ ] Add a `ISSUE_TEMPLATE.md` file
- [ ] Add a `PULL_REQUEST_TEMPLATE.md` file
- [ ] Add tox.ini file to run tests in multiple environments
  - [x] Add py311 environment to run tests in python 3.11
  - [x] Add qc.cov environment to run coverage tests
  - [x] Add qc.sec environment to run security tests
  - [x] Add qc.sty environment to run style tests
  - [ ] Fix requirement of psycopg_binary for testing

# Cookiecutter Web Backend

Implemented using:

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Installation and run

There are 2 basic ways to install run the application:

- Using docker and docker-compose (recommended for production)

```bash
$ docker-compose up
```

This will run the application following the configuration in the `docker-compose.yml` file. It will also run a postgres database and a pgadmin instance to manage the database.

- Using poetry (recommended for development)

```bash
$ poetry install
```

This will run the application following the configuration in the `pyproject.toml` file. You can run your custom database or use the one in the `docker-compose.yml` file with the following command:

```bash
$ docker-compose up db
```

Then you can run the application with the following command:

```bash
$ ./scripts/load_environment.sh
$ poetry run uvicorn autoapp:app --reload
```

> If you use vscode, you can run the application in debug mode using the `Python: FastAPI` configuration. This loads the `.env` file automatically.
