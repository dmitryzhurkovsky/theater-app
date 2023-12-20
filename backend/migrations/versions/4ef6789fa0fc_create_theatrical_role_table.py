"""create theatrical_role table

Revision ID: 4ef6789fa0fc
Revises: 6616b8872c4a
Create Date: 2023-12-16 01:41:00.432334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ef6789fa0fc"
down_revision: Union[str, None] = "6616b8872c4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "theatrical_roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("theatrical_roles")
    # ### end Alembic commands ###
