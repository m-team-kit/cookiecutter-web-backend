from uuid import UUID

from pydantic import BaseModel

from .item import Item, ItemCreate, ItemInDB, ItemUpdate
from .msg import Msg
from .template import Template, TemplateCreate, TemplateInDB, TemplateUpdate
from .token import Token, TokenPayload
from .user import User, UserCreate, UserInDB, UserUpdate


class Option(BaseModel):
    option: str
    description: str


class Project(BaseModel):
    code: UUID
    link: str
