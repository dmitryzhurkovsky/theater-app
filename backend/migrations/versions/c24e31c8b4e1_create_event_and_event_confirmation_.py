"""create_event_and_event_confirmation_tables

Revision ID: c24e31c8b4e1
Revises: 18a32d542445
Create Date: 2024-04-28 12:23:53.706981

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

from src.core.database.utils import drop_enum, get_enum
from src.core.enums import EventTypeEnum, StatusTypeEnum

# revision identifiers, used by Alembic.
revision = "c24e31c8b4e1"
down_revision = "18a32d542445"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Uuid(), server_default=func.gen_random_uuid()),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column("place", sa.String(), nullable=False, server_default="scena"),
        sa.Column("event_type", get_enum("event_type_enum", EventTypeEnum), nullable=False),
        sa.Column(
            "status",
            get_enum("status_type_enum", StatusTypeEnum),
            nullable=False,
            server_default=StatusTypeEnum.PENDING,
        ),
        sa.Column("performance_id", sa.Uuid(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            server_onupdate=func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["performance_id"],
            ["performances.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index("idx_events_performance_id", "events", ["performance_id"])

    op.create_table(
        "event_confirmations",
        sa.Column("id", sa.Uuid(), server_default=func.gen_random_uuid()),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("is_approved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            server_onupdate=func.now(),
        ),
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
        sa.UniqueConstraint("user_id", "event_id", name="idx_user_event"),
    )


def downgrade() -> None:
    op.drop_index("idx_events_performance_id", table_name="events")

    op.drop_table("event_confirmations")
    op.drop_table("events")

    drop_enum("event_type_enum")
    drop_enum("status_type_enum")
