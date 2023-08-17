"""
The OpenAPI 3.0 specification for the REST API of the Software Templates Hub:
Create your project from cookiecutter templates via web interface:
[https://templates.services.fedcloud.eu](https://templates.services.fedcloud.eu)

- [Templates Hub](https://templates.services.fedcloud.eu)
- [How to add your template to the Hub](https://github.com/m-team-kit/templates-hub/blob/main/README.md)
"""
from fastapi import APIRouter

from app.api.v1.endpoints import templates, project, database

api_router = APIRouter()
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(database.router, prefix="/db", tags=["database"])
