"""create_performances_table

Revision ID: 5c387b42a9fc
Revises: 6616b8872c4a
Create Date: 2024-04-27 17:01:33.476873

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

from src.core.database.utils import drop_enum, get_enum
from src.core.enums import GenreTypeEnum

# revision identifiers, used by Alembic.
revision = "5c387b42a9fc"
down_revision = "6616b8872c4a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "performances",
        sa.Column("id", sa.Uuid(), server_default=func.gen_random_uuid()),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("director_id", sa.Uuid(), nullable=False),
        sa.Column("image", sa.String()),
        sa.Column("description", sa.String(length=1024)),
        sa.Column("about_author", sa.String(length=1024)),
        sa.Column("genre", get_enum("genre_type_enum", GenreTypeEnum), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("annotation", sa.String(length=1024)),
        sa.Column("recommendations", sa.JSON()),
        sa.Column("need_admin_approve", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            server_onupdate=func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
        sa.ForeignKeyConstraint(
            ["director_id"],
            ["users.id"],
        ),
    )


def downgrade() -> None:
    op.drop_table("performances")

    drop_enum("genre_type_enum")
