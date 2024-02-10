"""create events and performances table

Revision ID: b0b8be704576
Revises: 4c9e3982a64b
Create Date: 2024-02-01 08:52:51.262539

"""
from alembic import op
import sqlalchemy as sa


revision = "b0b8be704576"
down_revision = "4c9e3982a64b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.create_table(
        "events",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("place", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        
        sa.PrimaryKeyConstraint("id"),
    )
    
    op.create_table(
        "performances",
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=False),
        sa.Column("roles", sa.String(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )


def downgrade() -> None:
   
    op.drop_table("performances")
    op.drop_table("events")
