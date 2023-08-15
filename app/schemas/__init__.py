from uuid import UUID

from pydantic import BaseModel

from .template import Template, TemplateCreate, TemplateInDB, TemplateUpdate
from .user import User, UserCreate, UserInDB, UserUpdate


class Option(BaseModel):
    option: str
    description: str


class Project(BaseModel):
    code: UUID
    link: str
