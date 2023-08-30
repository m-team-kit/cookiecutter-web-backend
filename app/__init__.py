"""Description to be changed later at:
    - backend/app/__main__.py
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import app.core.authentication as auth
import app.core.database as db
import app.core.email_processor as email
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
    email.init_app(app)
    db.init_app(app)

    # Set "latest" api as mounted app
    _api_latests = FastAPI(description=api_v1.__doc__)
    _api_latests.state = app.state
    app.mount("/api/latest", _api_latests)
    _api_latests.include_router(api_v1.api_router)

    # Set "v1" api as mounted app
    _api_v1 = FastAPI(description=api_v1.__doc__)
    _api_v1.state = app.state
    app.mount("/api/v1", _api_v1)
    _api_v1.include_router(api_v1.api_router)

    # Return FastAPI instance
    return app
