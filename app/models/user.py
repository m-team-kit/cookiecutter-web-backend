"""Models for user related tables.

See SQLAlchemy documentation for information on how to work with the models.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base

if TYPE_CHECKING:
    from .template import Score  # noqa: F401


class User(Base):
    """User model definition."""

    subject: Mapped[str] = mapped_column(primary_key=True, index=True)
    issuer: Mapped[str] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)
    scores: Mapped[List["Score"]] = relationship(cascade="all, delete", passive_deletes=True)
    __table_args__ = (PrimaryKeyConstraint("subject", "issuer", name="id"), {})
