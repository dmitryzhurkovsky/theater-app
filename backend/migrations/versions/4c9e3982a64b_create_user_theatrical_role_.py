"""create user_theatrical_role_relationship table

Revision ID: 4c9e3982a64b
Revises: 4ef6789fa0fc
Create Date: 2023-12-16 01:46:26.170771

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4c9e3982a64b"
down_revision: Union[str, None] = "4ef6789fa0fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_theatrical_role_relationships",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("theatrical_role_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["theatrical_role_id"],
            ["theatrical_roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "theatrical_role_id", name="idx_user_theatrical_role"
        ),
    )


def downgrade() -> None:
    op.drop_table("user_theatrical_role_relationships")
