""""initial"

Revision ID: ec784700411b
Revises: 
Create Date: 2023-09-05 10:00:52.391838

"""
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ec784700411b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "template",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("repoFile", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("picture", sa.String(), nullable=False),
        sa.Column("gitLink", sa.String(), nullable=False),
        sa.Column("gitCheckout", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_template_id"), "template", ["id"], unique=False)
    op.create_index(op.f("ix_template_language"), "template", ["language"], unique=False)
    op.create_index(op.f("ix_template_repoFile"), "template", ["repoFile"], unique=False)
    op.create_table(
        "user",
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("issuer", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("subject", "issuer", name="id"),
    )
    op.create_index(op.f("ix_user_issuer"), "user", ["issuer"], unique=False)
    op.create_index(op.f("ix_user_subject"), "user", ["subject"], unique=False)
    op.create_table(
        "score",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("owner_subject", sa.String(), nullable=False),
        sa.Column("owner_issuer", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["owner_subject", "owner_issuer"], ["user.subject", "user.issuer"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["template.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_score_id"), "score", ["id"], unique=False)
    op.create_table(
        "tag",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["template.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tag_id"), "tag", ["id"], unique=False)
    op.create_index(op.f("ix_tag_name"), "tag", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tag_name"), table_name="tag")
    op.drop_index(op.f("ix_tag_id"), table_name="tag")
    op.drop_table("tag")
    op.drop_index(op.f("ix_score_id"), table_name="score")
    op.drop_table("score")
    op.drop_index(op.f("ix_user_subject"), table_name="user")
    op.drop_index(op.f("ix_user_issuer"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_template_repoFile"), table_name="template")
    op.drop_index(op.f("ix_template_language"), table_name="template")
    op.drop_index(op.f("ix_template_id"), table_name="template")
    op.drop_table("template")
    # ### end Alembic commands ###
