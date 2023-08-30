from typing import Set
from uuid import UUID

from pydantic import BaseModel


class Template(BaseModel, from_attributes=True):
    id: UUID
    repoFile: str
    title: str
    summary: str
    language: str
    tags: Set[str]
    picture: str
    gitLink: str
    gitCheckout: str
    score: float | None


class NotFound(BaseModel):
    detail: str = "Template not found."
