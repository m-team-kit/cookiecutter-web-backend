from fastapi import APIRouter

from app.api.v1.endpoints import templates, project, database

api_router = APIRouter()
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(database.router, prefix="/database", tags=["database"])
