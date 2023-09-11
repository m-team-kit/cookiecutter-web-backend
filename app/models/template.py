# pylint: disable=missing-module-docstring,missing-class-docstring,E1102
from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import utils
from app.database import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Template(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)
    repoFile: Mapped[str] = mapped_column(index=True)
    title: Mapped[str] = mapped_column()
    summary: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column(index=True)
    picture: Mapped[str] = mapped_column()
    gitLink: Mapped[str] = mapped_column()
    gitCheckout: Mapped[str] = mapped_column()
    score = hybrid_property(utils.score_calculation)
    scores: Mapped[List["Score"]] = relationship(cascade="all, delete", passive_deletes=True)
    _tags: Mapped[List["Tag"]] = relationship(collection_class=set, cascade="all, delete-orphan", passive_deletes=True)

    @property
    def tags(self) -> List[str]:  # pylint: disable=missing-function-docstring
        return set(tag.name for tag in self._tags)

    @tags.setter
    def tags(self, tags: List[str]) -> None:
        self._tags = set(Tag(name=tag) for tag in tags)


class Tag(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("template.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(index=True)


class Score(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("template.id", ondelete="CASCADE"))
    value: Mapped[float] = mapped_column()
    owner_subject: Mapped[str] = mapped_column()
    owner_issuer: Mapped[str] = mapped_column()
    owner_id = hybrid_property(lambda self: (self.owner_subject, self.owner_issuer))
    __table_args__ = (ForeignKeyConstraint(["owner_subject", "owner_issuer"], ["user.subject", "user.issuer"], ondelete="CASCADE"), {})
