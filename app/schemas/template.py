from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, validator

from app import models


# Shared properties
class TemplateBase(BaseModel):
    repoFile: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    language: Optional[str] = None
    tags: List[str] = []
    picture: Optional[str] = None
    gitLink: Optional[str] = None
    gitCheckout: Optional[str] = None
    score: Optional[float] = None


# Properties to receive on item creation
class TemplateCreate(TemplateBase):
    title: str


# Properties to receive on item update
class TemplateUpdate(TemplateBase):
    pass


# Properties shared by models stored in DB
class TemplateInDBBase(TemplateBase):
    id: UUID
    repoFile: str
    title: str
    summary: str
    language: str
    tags: List[str]
    picture: str
    gitLink: str
    gitCheckout: str
    score: float | None

    class Config:
        from_attributes = True


# Properties to return to client
class Template(TemplateInDBBase):
    pass

    @validator("tags", pre=True)
    @classmethod
    def item_name(cls, v: List[models.Tag]) -> List[str]:
        return [tag.name for tag in v]


# Properties properties stored in DB
class TemplateInDB(TemplateInDBBase):
    pass
