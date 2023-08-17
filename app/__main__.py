"""Description to be changed later at:
    - backend/app/__main__.py
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from app import api
from app.core.config import settings

# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=__doc__,
    openapi_url="/api/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Add favicon endpoint
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Favicon endpoint."""
    return FileResponse(settings.FAVICON_PATH, media_type="image/icon")


# Set "latest" api as mounted app
api_latests = FastAPI()
app.mount("/api/latest", api_latests)
api_latests.include_router(api.v1.api_router)


# Set "v1" api as mounted app
api_v1 = FastAPI()
app.mount("/api/v1", api_v1)
api_v1.include_router(api.v1.api_router)
