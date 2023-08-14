"""Description to be changed later at:
    - backend/app/main.py
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
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
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


# Set "latest" api as mounted app
api_latests = FastAPI()
app.mount("/latest", api_latests)
api_latests.include_router(api.example.api_router)


# Set "v1" api as mounted app
api_v1 = FastAPI()
app.mount("/v1", api_v1)
api_v1.include_router(api.v1.api_router)


# Set "example" api as mounted app
api_example = FastAPI()
app.mount("/example", api_example)
api_example.include_router(api.example.api_router)
