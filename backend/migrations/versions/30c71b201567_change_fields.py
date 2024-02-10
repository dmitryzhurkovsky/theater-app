"""change model fields

Revision ID: 30c71b201567
Revises: b0b8be704576
Create Date: 2024-02-05 09:13:38.547702

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "30c71b201567"
down_revision = "b0b8be704576"
branch_labels = None
depends_on = None


def upgrade() -> None:

    genretypeenum = postgresql.ENUM('COMEDY', 'TRAGEDY', 'DRAMA', 'FARCE', 'MUSICAL', 'THRILLER', 'POLITICAL', name='genretypeenum')
    genretypeenum.create(op.get_bind())
    op.add_column("events", sa.Column("is_approved", sa.Boolean(), nullable=False))
    op.add_column("events", sa.Column("performance_id", sa.Uuid(), nullable=False))
    
    op.drop_column("events", "status")
    op.drop_column("events", "performances_id")
    
    op.drop_constraint("events_performances_id_fkey", "events", type_="foreignkey")
    op.create_foreign_key(None, "events", "performances", ["performance_id"], ["id"])
 
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
    op.add_column("users", sa.Column("is_actor", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("is_director", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("free_dates", sa.DateTime(timezone=True), nullable=False))
    op.drop_column("users", "type")


def downgrade() -> None:
    
    op.add_column(
        "users",
        sa.Column(
            "type",
            postgresql.ENUM("ADMIN", "ACTOR", "VIEWER", name="roletypeenum"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("users", "free_dates")
    op.drop_column("users", "is_director")
    op.drop_column("users", "is_admin")
    op.drop_column("users", "is_actor")
    op.drop_column("performances", "need_admin_approve")
    op.drop_column("performances", "recommendations")
    op.drop_column("performances", "duration_min")
    op.drop_column("performances", "duration_hour")
    op.drop_column("performances", "age")
    op.drop_column("performances", "genre")
    op.drop_column("performances", "author_info")
    op.add_column(
        "events", sa.Column("performances_id", sa.UUID(), autoincrement=False, nullable=False)
    )
    op.add_column("events", sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key(
        "events_performances_id_fkey", "events", "performances", ["performances_id"], ["id"]
    )
    op.drop_column("events", "performance_id")
    op.drop_column("events", "is_approved")
    genretypeenum = postgresql.ENUM('COMEDY', 'TRAGEDY', 'DRAMA', 'FARCE', 'MUSICAL', 'THRILLER', 'POLITICAL', name='genretypeenum')
    genretypeenum.drop(op.get_bind())
