from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    pass


# Properties to receive via API on creation
class UserCreate(UserBase):
    subject: str
    issuer: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    issuer: Optional[str] = None
    subject: Optional[str] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass

    class Config:
        populate_by_name = True


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass
