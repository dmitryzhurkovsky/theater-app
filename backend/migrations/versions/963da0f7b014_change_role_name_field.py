"""change_role_name_field

Revision ID: 963da0f7b014
Revises: 2adc0a8a86c2
Create Date: 2024-03-05 07:41:05.435907

"""
from alembic import op
import sqlalchemy as sa

revision = "963da0f7b014"
down_revision = "2adc0a8a86c2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("theatrical_roles", sa.Column("role_name", sa.String(), nullable=False))
    op.create_unique_constraint("ix_theatrical_roles_role_name", "theatrical_roles", ["role_name"])
    op.drop_column("theatrical_roles", "name")
    op.drop_column("theatrical_roles", "actors")
    op.add_column("theatrical_roles", sa.Column("actors", sa.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    op.drop_column("theatrical_roles", "actors")
    op.add_column("theatrical_roles", sa.Column("actors", sa.ARRAY(sa.VARCHAR()), nullable=True))
    op.add_column("theatrical_roles", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint("ix_theatrical_roles_role_name", "theatrical_roles", type_="unique")
    op.drop_column("theatrical_roles", "role_name")
