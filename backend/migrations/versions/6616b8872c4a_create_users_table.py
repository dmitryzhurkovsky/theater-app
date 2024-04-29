"""create users table

Revision ID: 6616b8872c4a
Revises:
Create Date: 2023-12-16 01:37:17.603183

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6616b8872c4a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), server_default=func.gen_random_uuid()),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("gender", sa.Enum("MAN", "WOMAN", "NA", name="gendertypeenum"), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("photo", sa.String()),
        sa.Column("birth_date", sa.Date()),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "user_roles",
            postgresql.ARRAY(sa.Enum("ADMIN", "ACTOR", "DIRECTOR", "VIEWER", name="userroletypeenum")),
            nullable=False,
        ),
        sa.Column("viber_link", sa.String()),
        sa.Column("telegram_link", sa.String()),
        sa.Column("instagram_link", sa.String()),
        sa.Column("free_dates", postgresql.ARRAY(sa.Date())),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            server_onupdate=func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone_number"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("instagram_link"),
        sa.UniqueConstraint("telegram_link"),
        sa.UniqueConstraint("viber_link"),
    )


def downgrade() -> None:
    op.drop_table("users")

    gendertypeenum = postgresql.ENUM("MAN", "WOMAN", "NA", name="gendertypeenum")
    gendertypeenum.drop(op.get_bind())

    userroletypeenum = postgresql.ENUM("ADMIN", "ACTOR", "DIRECTOR", "VIEWER", name="userroletypeenum")
    userroletypeenum.drop(op.get_bind())
