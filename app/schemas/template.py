from typing import Optional

from pydantic import BaseModel


# Shared properties
class TemplateBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class TemplateCreate(TemplateBase):
    title: str


# Properties to receive on item update
class TemplateUpdate(TemplateBase):
    pass


# Properties shared by models stored in DB
class TemplateInDBBase(TemplateBase):
    id: int
    title: str
    owner_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Template(TemplateInDBBase):
    pass


# Properties properties stored in DB
class TemplateInDB(TemplateInDBBase):
    pass
