"""create_notifications_table

Revision ID: c7d5900a949a
Revises: c24e31c8b4e1
Create Date: 2024-04-28 13:20:59.228153

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

from src.core.database.utils import drop_enum, get_enum
from src.core.enums import NotificationTypeEnum

# revision identifiers, used by Alembic.
revision = "c7d5900a949a"
down_revision = "c24e31c8b4e1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.Uuid(), server_default=func.gen_random_uuid()),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("type", get_enum("notification_type_enum", NotificationTypeEnum), nullable=False),
        sa.Column("text", sa.String(length=1024)),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("notifications")

    drop_enum("notification_type_enum")
