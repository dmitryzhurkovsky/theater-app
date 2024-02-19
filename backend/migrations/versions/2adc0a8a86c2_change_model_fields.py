"""change model fields

Revision ID: 2adc0a8a86c2
Revises: b0b8be704576
Create Date: 2024-02-11 12:45:29.013800

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2adc0a8a86c2"
down_revision = "b0b8be704576"
branch_labels = None
depends_on = None


def upgrade() -> None:
    genretypeenum = postgresql.ENUM(
        "COMEDY", "TRAGEDY", "DRAMA", "FARCE", "MUSICAL", "THRILLER", "POLITICAL", name="genretypeenum"
    )
    genretypeenum.create(op.get_bind())

    op.create_table(
        "user_theatrical_role_relationship",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("theatrical_role_id", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["theatrical_role_id"],
            ["theatrical_roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("user_theatrical_role_relationships")

    op.add_column("events", sa.Column("is_approved", sa.Boolean(), nullable=False))
    op.add_column("events", sa.Column("performance_id", sa.Uuid(), nullable=False))
    op.create_index(op.f("ix_events_performance_id"), "events", ["performance_id"], unique=False)
    op.create_foreign_key("events_performances", "events", "performances", ["performance_id"], ["id"])
    op.drop_column("events", "status")

    op.add_column("performances", sa.Column("author_info", sa.String(length=1024), nullable=False))
    op.add_column(
        "performances",
        sa.Column(
            "genre",
            sa.Enum(
                "COMEDY",
                "TRAGEDY",
                "DRAMA",
                "FARCE",
                "MUSICAL",
                "THRILLER",
                "POLITICAL",
                name="genretypeenum",
            ),
            nullable=False,
        ),
    )
    op.add_column("performances", sa.Column("age", sa.Integer(), nullable=False))
    op.add_column("performances", sa.Column("duration_hour", sa.Integer(), nullable=False))
    op.add_column("performances", sa.Column("duration_min", sa.Integer(), nullable=False))
    op.add_column("performances", sa.Column("recommendations", sa.JSON(), nullable=False))
    op.add_column("performances", sa.Column("need_admin_approve", sa.Boolean(), nullable=False))
    op.drop_column("performances", "roles")

    op.add_column("theatrical_roles", sa.Column("event_id", sa.Uuid(), nullable=False))
    op.create_index(op.f("ix_theatrical_roles_event_id"), "theatrical_roles", ["event_id"], unique=False)
    op.create_foreign_key("theatrical_roles_events", "theatrical_roles", "events", ["event_id"], ["id"])
    op.add_column("theatrical_roles", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column("theatrical_roles", sa.Column("actors", sa.ARRAY(sa.VARCHAR()), nullable=True))

    op.add_column("users", sa.Column("is_actor", sa.Boolean(), nullable=False, default=True))
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), nullable=False, default=False))
    op.add_column("users", sa.Column("is_director", sa.Boolean(), nullable=False, default=False))
    op.add_column("users", sa.Column("free_dates", sa.ARRAY(sa.DateTime(timezone=True)), nullable=True, default=None))


def downgrade() -> None:
    op.drop_column("users", "free_dates")
    op.drop_column("users", "is_director")
    op.drop_column("users", "is_admin")
    op.drop_column("users", "is_actor")

    op.drop_column("theatrical_roles", "name")
    op.drop_index(op.f("ix_theatrical_roles_event_id"), table_name="theatrical_roles")
    op.drop_column("theatrical_roles", "event_id")
    op.drop_column("theatrical_roles", "actors")

    op.add_column("performances", sa.Column("roles", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column("performances", "need_admin_approve")
    op.drop_column("performances", "recommendations")
    op.drop_column("performances", "duration_min")
    op.drop_column("performances", "duration_hour")
    op.drop_column("performances", "age")
    op.drop_column("performances", "genre")
    op.drop_column("performances", "author_info")

    op.add_column("events", sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f("ix_events_performance_id"), table_name="events")
    op.drop_column("events", "performance_id")
    op.drop_column("events", "is_approved")
    op.create_table(
        "user_theatrical_role_relationships",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("theatrical_role_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["theatrical_role_id"],
            ["theatrical_roles.id"],
            name="user_theatrical_role_relationships_theatrical_role_id_fkey",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="user_theatrical_role_relationships_user_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="user_theatrical_role_relationships_pkey"),
    )
    op.drop_table("user_theatrical_role_relationship")

    genretypeenum = postgresql.ENUM(
        "COMEDY", "TRAGEDY", "DRAMA", "FARCE", "MUSICAL", "THRILLER", "POLITICAL", name="genretypeenum"
    )
    genretypeenum.drop(op.get_bind())
