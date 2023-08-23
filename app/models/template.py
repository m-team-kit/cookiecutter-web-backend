from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.utils import score_calculation

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
    tags: Mapped[List["Tag"]] = relationship(collection_class=set, cascade="all, delete", passive_deletes=True)
    picture: Mapped[str] = mapped_column()
    gitLink: Mapped[str] = mapped_column()
    gitCheckout: Mapped[str] = mapped_column()
    score = hybrid_property(score_calculation)
    scores: Mapped[List["Score"]] = relationship(cascade="all, delete", passive_deletes=True)


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
    __table_args__ = (ForeignKeyConstraint(["owner_subject", "owner_issuer"], ["user.subject", "user.issuer"], ondelete="CASCADE"), {})
