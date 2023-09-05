"""Description to be changed later at:
    - backend/app/__main__.py
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware

import app.core.authentication as auth
import app.core.database as db
from app import api_v1
from app.config import Settings


# Application Factories
# https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories
def create_app(**custom_parameters) -> FastAPI:
    """Create FastAPI instance."""
    app = FastAPI()  # pylint: disable=redefined-outer-name
    app.state.settings = Settings(**custom_parameters)
    app.title = app.state.settings.project_name
    app.description = __doc__
    app.openapi_url = "/api/openapi.json"
    app.separate_input_output_schemas = False

    # Set all CORS enabled origins
    origins = [str(origin) for origin in app.state.settings.cors_origins]
    if origins is not []:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

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
