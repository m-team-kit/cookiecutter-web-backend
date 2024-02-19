"""Cookiecutter Web Backend for AI4EOSC initializer. This module initializes
the FastAPI application and mounts the API versions to the main app. Also it
the root package for the application.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware

import app.authentication as auth
import app.database as db
from app import api_v1, config


# Application Factories
# https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories
def create_app(**custom_parameters) -> FastAPI:
    """Create FastAPI instance."""
    app = FastAPI()  # pylint: disable=redefined-outer-name
    config.set_settings(app, **custom_parameters)

    # Set security configuration
    auth.init_app(app)
    db.init_app(app)

    # Mount API versions to the main app
    mount_api(api_v1, app, "/api/latest")
    mount_api(api_v1, app, "/api/v1")

    # Favicon route
    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return FileResponse(Path(__file__).parent / "../favicon.ico")

    # Redirect to latest API version
    @app.get("/", include_in_schema=False)
    async def redirect_to_latest():
        return RedirectResponse(url="/api/latest/docs")

    # Return FastAPI instance
    return app


def mount_api(package, app: FastAPI, prefix: str) -> None:
    """Mount an API to the main app."""
    api = FastAPI(description=package.__doc__)
    api.separate_input_output_schemas = False
    api.state = app.state
    app.mount(prefix, api)
    api.include_router(package.api_router)
    package.add_exception_handlers(api)
    config.set_cors(api, app.state.settings)
