"""create_performance_roles_tables

Revision ID: 18a32d542445
Revises: 5c387b42a9fc
Create Date: 2024-04-28 09:37:30.341083

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision = "18a32d542445"
down_revision = "5c387b42a9fc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "performance_roles",
        sa.Column("id", sa.Uuid(), server_default=func.gen_random_uuid()),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("performance_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["performance_id"],
            ["performances.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("title", "performance_id", name="uq_title_performance_id"),
    )
    op.create_index("idx_performance_roles_performance_id", "performance_roles", ["performance_id"])

    op.create_table(
        "user_performance_role_relationship",
        sa.Column("id", sa.Uuid(), server_default=func.gen_random_uuid()),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("performance_role_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["performance_role_id"],
            ["performance_roles.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("user_id", "performance_role_id", name="uq_user_theatrical_role"),
    )
    op.create_index("idx_user_performance_role_relationship_user_id", "user_performance_role_relationship", ["user_id"])


def downgrade() -> None:
    op.drop_index("idx_performance_roles_performance_id", table_name="performance_roles")
    op.drop_index("idx_user_performance_role_relationship_user_id", table_name="user_performance_role_relationship")

    op.drop_table("user_performance_role_relationship")
    op.drop_table("performance_roles")
