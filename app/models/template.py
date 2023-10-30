"""Models for template related tables."""
# pylint: disable=missing-class-docstring,E1102
# pylint: disable=missing-function-docstring
from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import orm, sql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext import associationproxy as ap
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import Base, UniqueMixin


class Template(Base):
    id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    modified: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=sql.func.now(), server_onupdate=sql.func.now(), nullable=False)
    repoFile: orm.Mapped[str] = orm.mapped_column(index=True, nullable=False)
    title: orm.Mapped[str] = orm.mapped_column(nullable=False)
    summary: orm.Mapped[str] = orm.mapped_column(nullable=False)
    picture: orm.Mapped[str] = orm.mapped_column(nullable=True)
    gitLink: orm.Mapped[str] = orm.mapped_column(nullable=False)
    feedback: orm.Mapped[str] = orm.mapped_column(nullable=False)
    gitCheckout: orm.Mapped[str] = orm.mapped_column(nullable=True)
    scores: orm.Mapped[list["Score"]] = orm.relationship(cascade="all, delete", passive_deletes=True)
    score: orm.Mapped[float] = orm.mapped_column(nullable=True)
    tag_associations: orm.Mapped[set["TagAssociation"]] = orm.relationship(back_populates="template", cascade="all, delete-orphan")
    tags: ap.AssociationProxy[set["Tag"]] = ap.association_proxy("tag_associations", "name", creator=lambda x: TagAssociation(name=x))


class TagAssociation(Base):
    template_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("template.id", ondelete="CASCADE"), primary_key=True)
    tag_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)
    template: orm.Mapped["Template"] = orm.relationship(back_populates="tag_associations")
    tag: orm.Mapped["Tag"] = orm.relationship()
    name: ap.AssociationProxy[str] = ap.association_proxy("tag", "name", creator=lambda x: Tag(name=x.lower()))

    @orm.validates("tag")  # https://github.com/sqlalchemy/sqlalchemy/wiki/UniqueObjectValidatedOnPending
    def validate_tag(self, key, tag):
        session = orm.object_session(self)
        if session is None:
            return tag  # pragma: no cover
        return setup_tag(session, tag.name)


class Tag(UniqueMixin, Base):
    id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name: orm.Mapped[str] = orm.mapped_column(index=True, unique=True)

    @classmethod
    def unique_hash(cls, name):  # pylint: disable=arguments-differ
        return name

    @classmethod
    def unique_filter(cls, query, name):  # pylint: disable=arguments-differ
        return query.filter(cls.name == name)


class Score(Base):
    id: orm.Mapped[UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    modified: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=sql.func.now(), server_onupdate=sql.func.now(), nullable=False)
    parent_id: orm.Mapped[UUID] = orm.mapped_column(sa.ForeignKey("template.id", ondelete="CASCADE"))
    value: orm.Mapped[float] = orm.mapped_column()
    owner_subject: orm.Mapped[str] = orm.mapped_column()
    owner_issuer: orm.Mapped[str] = orm.mapped_column()
    owner_id = hybrid_property(lambda self: (self.owner_subject, self.owner_issuer))
    __table_args__ = (sa.ForeignKeyConstraint(["owner_subject", "owner_issuer"], ["user.subject", "user.issuer"], ondelete="CASCADE"), {})


@sa.event.listens_for(orm.Session, "transient_to_pending")
def validate_tag(session, association):
    if isinstance(association, TagAssociation) and association.tag is not None and association.tag.id is None:
        old_type = association.tag  # the id-less Type object that got created
        if old_type in session:  # make sure it's not going to be persisted.
            session.expunge(old_type)
        association.tag = setup_tag(session, association.tag.name)


def setup_tag(session, name):
    with session.no_autoflush:
        return Tag.as_unique(session, name=name)
