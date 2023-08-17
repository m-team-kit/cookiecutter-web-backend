from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Template(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    repoFile: Mapped[str] = mapped_column(index=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)
    title: Mapped[str] = mapped_column()
    summary: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column(index=True)
    tags: Mapped[List["Tag"]] = relationship(cascade="all, delete")
    picture: Mapped[str] = mapped_column()
    gitLink: Mapped[str] = mapped_column()
    gitCheckout: Mapped[str] = mapped_column()
    score = hybrid_property(lambda self: sum(score.value for score in self.scores) / len(self.scores))
    scores: Mapped[List["Score"]] = relationship(cascade="all, delete")


class Tag(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("template.id"))
    name: Mapped[str] = mapped_column(index=True, unique=True)


class Score(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("template.id"))
    value: Mapped[float] = mapped_column()
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), unique=True)
