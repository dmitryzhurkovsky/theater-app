"""create users table

Revision ID: 6616b8872c4a
Revises:
Create Date: 2023-12-16 01:37:17.603183

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6616b8872c4a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("gender", sa.Enum("MAN", "WOMAN", name="gendertypeenum"), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("birth_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("photo", sa.String(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("ADMIN", "ACTOR", "VIEWER", name="roletypeenum"),
            nullable=False,
        ),
        sa.Column("viber_link", sa.String(), nullable=True),
        sa.Column("telegram_link", sa.String(), nullable=True),
        sa.Column("instagram_link", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("instagram_link"),
        sa.UniqueConstraint("telegram_link"),
        sa.UniqueConstraint("viber_link"),
    )


def downgrade() -> None:
    op.drop_table("users")
