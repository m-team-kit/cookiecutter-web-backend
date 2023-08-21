from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Token

if TYPE_CHECKING:
    from .template import Score  # noqa: F401


class User(Token):
    subject: Mapped[str] = mapped_column(primary_key=True, index=True)
    issuer: Mapped[str] = mapped_column(primary_key=True, index=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)
    scores: Mapped[List["Score"]] = relationship(cascade="all, delete")
