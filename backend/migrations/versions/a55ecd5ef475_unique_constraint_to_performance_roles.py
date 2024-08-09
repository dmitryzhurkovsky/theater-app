"""Add composite unique constraint to performance_roles table

Revision ID: a55ecd5ef475
Revises: f24211d46708
Create Date: 2024-08-09 13:52:12.498942

"""
from alembic import op

revision = "a55ecd5ef475"
down_revision = "f24211d46708"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_title_performance_id", "performance_roles", ["title", "performance_id"])


def downgrade() -> None:
    op.drop_constraint("uq_title_performance_id", "performance_roles", type_="unique")
