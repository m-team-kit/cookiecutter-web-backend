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
